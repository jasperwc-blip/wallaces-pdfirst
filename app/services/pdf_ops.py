from __future__ import annotations

import io
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from app.core.page_ranges import PageRange, parse_page_ranges


def ensure_pdf_readable(path: str | Path) -> PdfReader:
    reader = PdfReader(str(path))
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise ValueError("PDF is encrypted and cannot be opened without a password.") from exc
    return reader


def image_files_to_pdf(
    image_paths: Iterable[str | Path],
    output_pdf: str | Path,
    mode: str = "fit_a4",
    orientation: str = "portrait",
    margin: float = 36,
) -> Path:
    paths = [Path(p) for p in image_paths]
    if not paths:
        raise ValueError("Select at least one image.")
    output = Path(output_pdf)
    output.parent.mkdir(parents=True, exist_ok=True)
    page_size = _oriented_page_size(A4, orientation)

    c = canvas.Canvas(str(output), pagesize=page_size)
    for path in paths:
        with Image.open(path) as img:
            img = _normalize_image(ImageOps.exif_transpose(img))
            if mode == "preserve":
                width, height = _oriented_page_size(img.size, orientation)
                c.setPageSize((width, height))
                draw_w, draw_h = _fit_size(img.width, img.height, width, height)
                preview = _scaled_for_pdf(img, draw_w, draw_h)
                c.drawImage(ImageReader(preview), (width - draw_w) / 2, (height - draw_h) / 2, width=draw_w, height=draw_h)
            else:
                c.setPageSize(page_size)
                page_w, page_h = page_size
                max_w = max(1, page_w - margin * 2)
                max_h = max(1, page_h - margin * 2)
                draw_w, draw_h = _fit_size(img.width, img.height, max_w, max_h)
                preview = _scaled_for_pdf(img, draw_w, draw_h)
                x = (page_w - draw_w) / 2
                y = (page_h - draw_h) / 2
                c.drawImage(ImageReader(preview), x, y, width=draw_w, height=draw_h)
            c.showPage()
    c.save()
    return output


def merge_pdfs(pdf_paths: Iterable[str | Path], output_pdf: str | Path) -> Path:
    paths = [Path(p) for p in pdf_paths]
    if len(paths) < 2:
        raise ValueError("Select at least two PDFs to merge.")
    writer = PdfWriter()
    for path in paths:
        reader = ensure_pdf_readable(path)
        for page in reader.pages:
            writer.add_page(page)
    return _write_pdf(writer, output_pdf)


def split_pdf_by_ranges(input_pdf: str | Path, ranges: Iterable[PageRange], output_dir: str | Path, prefix: str = "split") -> list[Path]:
    reader = ensure_pdf_readable(input_pdf)
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for index, page_range in enumerate(ranges, start=1):
        writer = PdfWriter()
        for page_num in range(page_range.start - 1, page_range.end):
            writer.add_page(reader.pages[page_num])
        label = page_range.label or f"{page_range.start}-{page_range.end}"
        output = output_root / f"{prefix}_range_{index}_{label}.pdf"
        _write_pdf(writer, output)
        outputs.append(output)
    return outputs


def split_pdf_by_range_text(input_pdf: str | Path, range_text: str, output_dir: str | Path) -> list[Path]:
    total = len(ensure_pdf_readable(input_pdf).pages)
    return split_pdf_by_ranges(input_pdf, parse_page_ranges(range_text, total), output_dir)


def split_pdf_by_mode(input_pdf: str | Path, output_dir: str | Path, mode: str, range_text: str = "") -> list[Path]:
    reader = ensure_pdf_readable(input_pdf)
    total = len(reader.pages)
    if mode == "custom_ranges":
        return split_pdf_by_ranges(input_pdf, parse_page_ranges(range_text, total), output_dir)
    if mode == "burst_single_pages":
        ranges = [PageRange(i, i, str(i)) for i in range(1, total + 1)]
    elif mode == "even_pages":
        ranges = [PageRange(i, i, str(i)) for i in range(2, total + 1, 2)]
    elif mode == "odd_pages":
        ranges = [PageRange(i, i, str(i)) for i in range(1, total + 1, 2)]
    else:
        raise ValueError("Unknown split mode.")
    return split_pdf_by_ranges(input_pdf, ranges, output_dir, prefix=mode)


def rotate_pdf(input_pdf: str | Path, output_pdf: str | Path, angle: int, page_ranges: str = "1-end") -> Path:
    if angle not in {90, 180, 270}:
        raise ValueError("Rotation angle must be 90, 180, or 270 degrees.")
    reader = ensure_pdf_readable(input_pdf)
    selected = set()
    for item in parse_page_ranges(page_ranges, len(reader.pages), allow_overlap=True):
        selected.update(range(item.start, item.end + 1))
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        if idx in selected:
            page.rotate(angle)
        writer.add_page(page)
    return _write_pdf(writer, output_pdf)


def add_text_watermark(
    input_pdf: str | Path,
    output_pdf: str | Path,
    text: str,
    font_size: int = 48,
    opacity: float = 0.25,
    rotation: float = 35,
    position: str = "center",
    page_ranges: str = "1-end",
    font_name: str = "Helvetica",
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    color: tuple[float, float, float] = (0.8, 0, 0),
) -> Path:
    reader = ensure_pdf_readable(input_pdf)
    selected = _selected_pages(page_ranges, len(reader.pages))
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        if idx in selected:
            watermark = _make_text_watermark(page, text, font_size, opacity, rotation, position, font_name, bold, italic, underline, color)
            page.merge_page(watermark.pages[0])
        writer.add_page(page)
    return _write_pdf(writer, output_pdf)


def add_image_watermark(
    input_pdf: str | Path,
    output_pdf: str | Path,
    image_path: str | Path,
    opacity: float = 0.3,
    scale: float = 0.35,
    position: str = "center",
    page_ranges: str = "1-end",
) -> Path:
    reader = ensure_pdf_readable(input_pdf)
    selected = _selected_pages(page_ranges, len(reader.pages))
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        if idx in selected:
            watermark = _make_image_watermark(page, image_path, opacity, scale, position)
            page.merge_page(watermark.pages[0])
        writer.add_page(page)
    return _write_pdf(writer, output_pdf)


def remove_pdf_annotations(input_pdf: str | Path, output_pdf: str | Path) -> Path:
    reader = ensure_pdf_readable(input_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        if "/Annots" in page:
            del page["/Annots"]
        writer.add_page(page)
    return _write_pdf(writer, output_pdf)


def _normalize_image(img: Image.Image) -> Image.Image:
    if img.mode in {"RGBA", "LA"}:
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.getchannel("A"))
        return bg
    return img.convert("RGB")


def _oriented_page_size(size: tuple[float, float], orientation: str) -> tuple[float, float]:
    width, height = size
    if orientation == "landscape" and height > width:
        return height, width
    if orientation == "portrait" and width > height:
        return height, width
    return width, height


def _fit_size(src_w: float, src_h: float, max_w: float, max_h: float) -> tuple[float, float]:
    scale = min(max_w / src_w, max_h / src_h)
    return src_w * scale, src_h * scale


def _scaled_for_pdf(img: Image.Image, draw_w: float, draw_h: float) -> Image.Image:
    max_pixels = 3_000_000
    target_w = max(1, int(draw_w * 2))
    target_h = max(1, int(draw_h * 2))
    if target_w * target_h > max_pixels:
        ratio = (max_pixels / (target_w * target_h)) ** 0.5
        target_w = max(1, int(target_w * ratio))
        target_h = max(1, int(target_h * ratio))
    if img.width <= target_w and img.height <= target_h:
        return img
    resized = img.copy()
    resized.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
    return resized


def _selected_pages(page_ranges: str, total_pages: int) -> set[int]:
    selected: set[int] = set()
    for item in parse_page_ranges(page_ranges, total_pages, allow_overlap=True):
        selected.update(range(item.start, item.end + 1))
    return selected


def _page_size(page) -> tuple[float, float]:
    box = page.mediabox
    return float(box.width), float(box.height)


def _make_text_watermark(
    page,
    text: str,
    font_size: int,
    opacity: float,
    rotation: float,
    position: str,
    font_name: str,
    bold: bool,
    italic: bool,
    underline: bool,
    color: tuple[float, float, float],
) -> PdfReader:
    width, height = _page_size(page)
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.saveState()
    c.setFillColor(colors.Color(color[0], color[1], color[2], alpha=max(0, min(opacity, 1))))
    resolved_font = _resolve_pdf_font(font_name, bold, italic)
    c.setFont(resolved_font, font_size)
    if position == "tiled":
        for x in range(0, int(width) + 200, 260):
            for y in range(0, int(height) + 200, 180):
                c.saveState()
                c.translate(x, y)
                c.rotate(rotation)
                _draw_watermark_text(c, text, 0, 0, font_size, underline)
                c.restoreState()
    else:
        x, y = _position_xy(position, width, height, 90, 40)
        c.translate(x, y)
        c.rotate(rotation)
        _draw_watermark_text(c, text, 0, 0, font_size, underline)
    c.restoreState()
    c.save()
    packet.seek(0)
    return PdfReader(packet)


def _resolve_pdf_font(font_name: str, bold: bool, italic: bool) -> str:
    base = "Courier" if font_name.lower().startswith("courier") else "Times-Roman" if font_name.lower().startswith("times") else "Helvetica"
    if base == "Times-Roman":
        if bold and italic:
            return "Times-BoldItalic"
        if bold:
            return "Times-Bold"
        if italic:
            return "Times-Italic"
        return base
    if bold and italic:
        return f"{base}-BoldOblique"
    if bold:
        return f"{base}-Bold"
    if italic:
        return f"{base}-Oblique"
    return base


def _draw_watermark_text(c: canvas.Canvas, text: str, x: float, y: float, font_size: int, underline: bool) -> None:
    c.drawCentredString(x, y, text)
    if underline:
        text_width = c.stringWidth(text)
        c.setLineWidth(max(1, font_size / 18))
        c.line(x - text_width / 2, y - font_size * 0.18, x + text_width / 2, y - font_size * 0.18)


def _make_image_watermark(page, image_path: str | Path, opacity: float, scale: float, position: str) -> PdfReader:
    width, height = _page_size(page)
    with Image.open(image_path) as img:
        img = _normalize_image(img).convert("RGBA")
        alpha = img.getchannel("A")
        alpha = alpha.point(lambda p: int(p * max(0, min(opacity, 1))))
        img.putalpha(alpha)
        draw_w = width * max(0.05, min(scale, 1.5))
        draw_h = draw_w * img.height / img.width
        x, y = _position_xy(position, width, height, draw_w, draw_h)
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))
        c.drawImage(ImageReader(img), x, y, width=draw_w, height=draw_h, mask="auto")
        c.save()
        packet.seek(0)
        return PdfReader(packet)


def _position_xy(position: str, page_w: float, page_h: float, item_w: float, item_h: float) -> tuple[float, float]:
    pad = 36
    positions = {
        "top-left": (pad, page_h - item_h - pad),
        "top-right": (page_w - item_w - pad, page_h - item_h - pad),
        "bottom-left": (pad, pad),
        "bottom-right": (page_w - item_w - pad, pad),
        "center": ((page_w - item_w) / 2, (page_h - item_h) / 2),
    }
    return positions.get(position, positions["center"])


def _write_pdf(writer: PdfWriter, output_pdf: str | Path) -> Path:
    output = Path(output_pdf)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as fh:
        writer.write(fh)
    return output
