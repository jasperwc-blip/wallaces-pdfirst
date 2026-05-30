from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from app.services.pdf_ops import ensure_pdf_readable


@dataclass
class MarkResult:
    question: str
    student_answer: str
    correct_answer: str
    score: float
    max_score: float
    comment: str
    confidence: str


def parse_answer_bank(path: str | Path) -> dict[str, str]:
    source = Path(path)
    suffix = source.suffix.lower()
    if suffix == ".json":
        data = json.loads(source.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in data.items()}
    if suffix == ".csv":
        with source.open(newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            return {str(row["question"]): str(row["answer"]) for row in reader}
    if suffix == ".pdf":
        text = _extract_pdf_text(source)
        return _parse_answer_lines(text)
    if suffix in {".jpg", ".jpeg", ".png"}:
        text = _extract_image_text(source)
        return _parse_answer_lines(text)
    if suffix not in {".txt", ".text"}:
        raise ValueError("Answer files must be JSON, CSV, TXT, PDF, JPG, or PNG.")
    return _parse_answer_lines(source.read_text(encoding="utf-8-sig", errors="replace"))


def _parse_answer_lines(text: str) -> dict[str, str]:
    answers: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.match(r"^(?:q(?:uestion)?\s*)?([A-Za-z0-9_.-]+)\s*[:),.-]\s*(.+)$", line, re.IGNORECASE)
        if not match:
            continue
        q, ans = match.groups()
        answers[q.strip()] = ans.strip()
    if not answers:
        raise ValueError("Could not parse any answers. Use lines like '1: A' or a JSON/CSV answer table.")
    return answers


def parse_student_answers(path: str | Path) -> dict[str, str]:
    return parse_answer_bank(path)


def _extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _extract_image_text(path: Path) -> str:
    try:
        import pytesseract  # type: ignore
        from PIL import Image

        with Image.open(path) as img:
            return pytesseract.image_to_string(img)
    except Exception as exc:
        raise ValueError(
            "Image answer extraction needs OCR. Install/bundle Tesseract and pytesseract, "
            "or use PDF/TXT/CSV/JSON for now."
        ) from exc


def mark_answers(
    student_answers: dict[str, str],
    answer_bank: dict[str, str],
    marks_per_question: float = 1.0,
    case_sensitive: bool = False,
) -> list[MarkResult]:
    results: list[MarkResult] = []
    for question, correct in answer_bank.items():
        student = student_answers.get(question, "")
        matched = _normalize(student, case_sensitive) == _normalize(correct, case_sensitive)
        score = marks_per_question if matched else 0.0
        results.append(
            MarkResult(
                question=question,
                student_answer=student,
                correct_answer=correct,
                score=score,
                max_score=marks_per_question,
                comment="Correct" if matched else "Review needed",
                confidence="high" if student else "low",
            )
        )
    return results


def export_results_json(results: list[MarkResult], output_json: str | Path) -> Path:
    output = Path(output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([asdict(item) for item in results], indent=2), encoding="utf-8")
    return output


def export_results_csv(results: list[MarkResult], output_csv: str | Path) -> Path:
    output = Path(output_csv)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(asdict(results[0]).keys()) if results else ["question"])
        writer.writeheader()
        for item in results:
            writer.writerow(asdict(item))
    return output


def create_marked_pdf(student_pdf: str | Path, results: list[MarkResult], output_pdf: str | Path) -> Path:
    reader = ensure_pdf_readable(student_pdf)
    writer = PdfWriter()
    total = sum(item.score for item in results)
    possible = sum(item.max_score for item in results)

    for page_index, page in enumerate(reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        overlay = _mark_overlay(width, height, results if page_index == 0 else [], total, possible, page_index == 0)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    output = Path(output_pdf)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as fh:
        writer.write(fh)
    return output


def _mark_overlay(width: float, height: float, results: list[MarkResult], total: float, possible: float, include_summary: bool) -> PdfReader:
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFillColor(colors.green)
    c.setFont("Helvetica-Bold", 18)
    if include_summary:
        c.drawString(36, height - 42, f"Score: {total:g}/{possible:g}")
        y = height - 74
        c.setFont("Helvetica", 10)
        for item in results[:30]:
            color = colors.green if item.score else colors.red
            c.setFillColor(color)
            symbol = "OK" if item.score else "X"
            c.drawString(42, y, f"{symbol} Q{item.question}: {item.score:g}/{item.max_score:g} - {item.comment}")
            y -= 14
    c.save()
    packet.seek(0)
    return PdfReader(packet)


def _normalize(value: str, case_sensitive: bool) -> str:
    value = " ".join(value.strip().split())
    return value if case_sensitive else value.lower()
