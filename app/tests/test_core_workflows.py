from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.core.page_ranges import parse_page_ranges
from app.services.marking import create_marked_pdf, mark_answers, parse_answer_bank
from app.services.pdf_ops import (
    add_image_watermark,
    add_text_watermark,
    image_files_to_pdf,
    merge_pdfs,
    remove_pdf_annotations,
    rotate_pdf,
    split_pdf_by_mode,
    split_pdf_by_range_text,
)
from app.services.transcript import parse_transcript, transcript_to_docx, transcript_to_pdf
from app.services.watermark_removal import remove_image_watermark_rectangles
from app.services.worksheet import clean_worksheet_pdf


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_page_range_parser(self) -> None:
        ranges = parse_page_ranges("1-1, 2-3, 4-end", 10)
        self.assertEqual([(r.start, r.end) for r in ranges], [(1, 1), (2, 3), (4, 10)])
        with self.assertRaises(ValueError):
            parse_page_ranges("1-3,3-4", 10)

    def test_image_to_pdf(self) -> None:
        images = [self._image(i) for i in range(3)]
        output = image_files_to_pdf(images, self.root / "images.pdf")
        self.assertEqual(len(PdfReader(str(output)).pages), 3)

    def test_image_to_pdf_respects_selected_orientation(self) -> None:
        portrait_image = self.root / "portrait.png"
        Image.new("RGB", (300, 700), "white").save(portrait_image)
        portrait = image_files_to_pdf([portrait_image], self.root / "portrait.pdf", orientation="portrait")
        landscape = image_files_to_pdf([portrait_image], self.root / "landscape.pdf", orientation="landscape")
        portrait_box = PdfReader(str(portrait)).pages[0].mediabox
        landscape_box = PdfReader(str(landscape)).pages[0].mediabox
        self.assertGreater(float(portrait_box.height), float(portrait_box.width))
        self.assertGreater(float(landscape_box.width), float(landscape_box.height))

    def test_transcript_outputs(self) -> None:
        vtt = self.root / "sample.vtt"
        vtt.write_text("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nSpeaker: Hello\n\n", encoding="utf-8")
        cues = parse_transcript(vtt, keep_timestamps=False)
        self.assertEqual(cues[0].text, "Speaker: Hello")
        docx = transcript_to_docx(vtt, self.root / "out.docx", keep_timestamps=False)
        pdf = transcript_to_pdf(vtt, self.root / "out.pdf", keep_timestamps=True)
        self.assertTrue(docx.exists())
        self.assertEqual(len(PdfReader(str(pdf)).pages), 1)

    def test_pdf_merge_split_rotate(self) -> None:
        pdfs = [self._pdf(f"p{i}.pdf", i) for i in (1, 2, 3)]
        merged = merge_pdfs(pdfs, self.root / "merged.pdf")
        self.assertEqual(len(PdfReader(str(merged)).pages), 6)
        ten = self._pdf("ten.pdf", 10)
        outputs = split_pdf_by_range_text(ten, "1-1,2-3,4-10", self.root / "split")
        self.assertEqual([len(PdfReader(str(p)).pages) for p in outputs], [1, 2, 7])
        odd_outputs = split_pdf_by_mode(ten, self.root / "odd", "odd_pages")
        even_outputs = split_pdf_by_mode(ten, self.root / "even", "even_pages")
        burst_outputs = split_pdf_by_mode(ten, self.root / "burst", "burst_single_pages")
        self.assertEqual(len(odd_outputs), 5)
        self.assertEqual(len(even_outputs), 5)
        self.assertEqual(len(burst_outputs), 10)
        rotated = rotate_pdf(ten, self.root / "rotated.pdf", 90)
        self.assertEqual(PdfReader(str(rotated)).pages[0].get("/Rotate"), 90)

    def test_watermarks(self) -> None:
        base = self._pdf("base.pdf", 1)
        text_marked = add_text_watermark(base, self.root / "text_watermark.pdf", "CONFIDENTIAL")
        image = self._image(99)
        image_marked = add_image_watermark(base, self.root / "image_watermark.pdf", image)
        self.assertEqual(len(PdfReader(str(text_marked)).pages), 1)
        self.assertEqual(len(PdfReader(str(image_marked)).pages), 1)

    def test_watermark_removal_image(self) -> None:
        img = Image.new("RGB", (240, 120), "white")
        draw = ImageDraw.Draw(img)
        draw.text((30, 45), "WATERMARK", fill=(0, 0, 0))
        source = self.root / "wm.png"
        img.save(source)
        output = remove_image_watermark_rectangles(source, self.root / "clean.png", [(20, 35, 190, 75)])
        self.assertTrue(output.exists())

    def test_worksheet_cleaning_removes_annotations(self) -> None:
        source = self._pdf_with_annotation()
        cleaned = clean_worksheet_pdf(source, self.root / "cleaned.pdf", ["student name"])
        self.assertNotIn("/Annots", PdfReader(str(cleaned)).pages[0])

    def test_marking_workflow(self) -> None:
        student_pdf = self._pdf("student.pdf", 1)
        bank = self.root / "bank.json"
        bank.write_text(json.dumps({"1": "A", "2": "B"}), encoding="utf-8")
        answers = {"1": "A", "2": "C"}
        results = mark_answers(answers, parse_answer_bank(bank))
        self.assertEqual(sum(r.score for r in results), 1)
        marked = create_marked_pdf(student_pdf, results, self.root / "marked.pdf")
        self.assertEqual(len(PdfReader(str(marked)).pages), 1)

    def _pdf(self, name: str, pages: int) -> Path:
        path = self.root / name
        c = canvas.Canvas(str(path), pagesize=A4)
        for i in range(1, pages + 1):
            c.drawString(72, 760, f"{name} page {i}")
            c.showPage()
        c.save()
        return path

    def _image(self, index: int) -> Path:
        path = self.root / f"image_{index}.png"
        img = Image.new("RGB", (300, 180), (80 + index, 120, 180))
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), f"Image {index}", fill="white")
        img.save(path)
        return path

    def _pdf_with_annotation(self) -> Path:
        from pypdf import PdfWriter
        from pypdf.annotations import FreeText

        base = self._pdf("annotated.pdf", 1)
        reader = PdfReader(str(base))
        writer = PdfWriter()
        writer.add_page(reader.pages[0])
        writer.add_annotation(0, FreeText(text="Answer: A", rect=(100, 650, 220, 700), font="Helvetica", font_size="12pt"))
        output = self.root / "annotated_answer.pdf"
        with output.open("wb") as fh:
            writer.write(fh)
        return output


if __name__ == "__main__":
    unittest.main()
