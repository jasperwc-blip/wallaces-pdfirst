from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from io import BytesIO
from dataclasses import dataclass
from pathlib import Path

from docx import Document
from pypdf import PdfReader

from app.core.page_ranges import parse_page_ranges


SCANNED_PDF_MESSAGE = (
    "This PDF appears to contain scanned images or non-extractable text. "
    "Use OCR PDF mode for scanned documents."
)
IMAGE_BASED_EDITABLE_WARNING = (
    "This PDF appears to be image-based or scanned. Editable text conversion may be limited. "
    "Use OCR PDF mode if an OCR engine is available."
)
OCR_NOT_ENABLED_MESSAGE = (
    "OCR PDF conversion is not currently enabled in this portable version. "
    "A bundled OCR engine is required before scanned PDFs can be converted into editable Word text."
)

MODE_EDITABLE = "Editable Word - layout-preserving"
MODE_OCR = "OCR PDF"
MODE_SIMPLE = "Simple text"
MODE_PPTX = "PDF to PPTX"


@dataclass(frozen=True)
class ConversionResult:
    success: bool
    message: str
    pages_processed: int
    extracted_character_count: int
    output_path: str


def convert_pdf_to_docx(
    input_pdf_path: str | Path,
    output_docx_path: str | Path,
    mode: str = MODE_EDITABLE,
    page_ranges: str = "1-end",
    ocr_language: str = "eng",
) -> ConversionResult:
    mode = _normalize_mode(mode)
    if mode == MODE_PPTX:
        from app.services.pdf_to_pptx import convert_pdf_to_pptx

        return convert_pdf_to_pptx(input_pdf_path, output_docx_path, page_ranges, ocr_language)
    if mode == MODE_OCR:
        return convert_pdf_to_docx_ocr(input_pdf_path, output_docx_path, page_ranges, ocr_language)
    if mode == MODE_SIMPLE:
        return convert_pdf_to_docx_simple(input_pdf_path, output_docx_path, page_ranges)
    return convert_pdf_to_docx_layout_preserving(input_pdf_path, output_docx_path, page_ranges)


def convert_pdf_to_docx_layout_preserving(input_pdf_path: str | Path, output_docx_path: str | Path, page_ranges: str = "1-end") -> ConversionResult:
    source = Path(input_pdf_path)
    output = _docx_path(output_docx_path, source)
    validation_error = _validate_paths(source, output)
    if validation_error:
        return ConversionResult(False, validation_error, 0, 0, str(output))

    page_count, _, scan_error = _pdf_text_stats(source)
    if scan_error:
        return ConversionResult(False, scan_error, page_count, 0, str(output))
    selected_pages, range_error = _selected_pages(page_ranges, page_count)
    if range_error:
        return ConversionResult(False, range_error, page_count, 0, str(output))
    selected_text_chars = _selected_char_count(source, selected_pages)
    if selected_text_chars == 0:
        return ConversionResult(False, IMAGE_BASED_EDITABLE_WARNING, len(selected_pages), 0, str(output))

    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        _run_pdf2docx_worker(source, output, [page - 1 for page in selected_pages])
    except Exception as exc:
        if output.exists():
            output.unlink()
        return ConversionResult(
            False,
            "Editable layout-preserving conversion failed. Try Simple text only for basic extraction, "
            f"or OCR PDF for scanned files if OCR is available. Details: {exc}",
            len(selected_pages),
            selected_text_chars,
            str(output),
        )

    if not output.exists() or output.stat().st_size == 0:
        return ConversionResult(False, "Editable layout-preserving conversion did not create a valid DOCX.", len(selected_pages), selected_text_chars, str(output))
    return ConversionResult(True, f"Converted PDF to editable layout-preserving Word: {output}", len(selected_pages), selected_text_chars, str(output))


def convert_pdf_to_docx_ocr(
    input_pdf_path: str | Path,
    output_docx_path: str | Path,
    page_ranges: str = "1-end",
    ocr_language: str = "eng",
) -> ConversionResult:
    source = Path(input_pdf_path)
    output = _docx_path(output_docx_path, source)
    validation_error = _validate_paths(source, output)
    if validation_error:
        return ConversionResult(False, validation_error, 0, 0, str(output))

    ocr_available, ocr_message = get_ocr_availability()
    if not ocr_available:
        return ConversionResult(False, ocr_message, 0, 0, str(output))

    page_count, _, scan_error = _pdf_text_stats(source)
    if scan_error:
        return ConversionResult(False, scan_error, page_count, 0, str(output))
    selected_pages, range_error = _selected_pages(page_ranges, page_count)
    if range_error:
        return ConversionResult(False, range_error, page_count, 0, str(output))

    try:
        import fitz
        import pytesseract
        from PIL import Image
    except Exception as exc:
        return ConversionResult(False, f"{OCR_NOT_ENABLED_MESSAGE} Python OCR wrapper is unavailable. Details: {exc}", len(selected_pages), 0, str(output))

    ocr_exe = configure_tesseract(pytesseract)

    try:
        pdf = fitz.open(str(source))
    except Exception as exc:
        return ConversionResult(False, f"Could not open PDF. It may be encrypted or corrupted. Details: {exc}", 0, 0, str(output))

    doc = Document()
    extracted_chars = 0
    try:
        matrix = fitz.Matrix(2.5, 2.5)
        for index, page_number in enumerate(selected_pages, start=1):
            if index > 1:
                doc.add_page_break()
            pixmap = pdf[page_number - 1].get_pixmap(matrix=matrix, alpha=False)
            image = Image.open(BytesIO(pixmap.tobytes("png")))
            text = pytesseract.image_to_string(image, lang=_normalize_ocr_language(ocr_language)).strip()
            extracted_chars += len(text)
            doc.add_heading(f"Page {page_number}", level=2)
            doc.add_paragraph(text if text else "[No OCR text detected on this page]")
        if extracted_chars == 0:
            return ConversionResult(False, OCR_NOT_ENABLED_MESSAGE, len(selected_pages), 0, str(output))
        output.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(output))
    except Exception as exc:
        if output.exists():
            output.unlink()
        return ConversionResult(False, f"{OCR_NOT_ENABLED_MESSAGE} Details: {exc}", len(selected_pages), extracted_chars, str(output))
    finally:
        pdf.close()

    return ConversionResult(True, f"Converted OCR PDF to Word: {output}", len(selected_pages), extracted_chars, str(output))


def _run_pdf2docx_worker(source: Path, output: Path, zero_based_pages: list[int]) -> None:
    pages_json = json.dumps(zero_based_pages)
    if getattr(sys, "frozen", False):
        cmd = [sys.executable, "--pdf2docx-worker", str(source), str(output), pages_json]
    else:
        cmd = [sys.executable, "-m", "app.pdf2docx_worker", str(source), str(output), pages_json]
    startupinfo = None
    creationflags = 0
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    completed = subprocess.run(
        cmd,
        cwd=str(Path(__file__).resolve().parents[2]),
        capture_output=True,
        text=True,
        startupinfo=startupinfo,
        creationflags=creationflags,
        timeout=900,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "pdf2docx worker failed").strip()
        raise RuntimeError(detail)


def convert_pdf_to_docx_simple(input_pdf_path: str | Path, output_docx_path: str | Path, page_ranges: str = "1-end") -> ConversionResult:
    source = Path(input_pdf_path)
    output = _docx_path(output_docx_path, source)
    validation_error = _validate_paths(source, output)
    if validation_error:
        return ConversionResult(False, validation_error, 0, 0, str(output))

    pages_text, error = _extract_page_text(source, page_ranges)
    if error:
        return ConversionResult(False, error, 0, 0, str(output))
    total_chars = sum(len(text) for text in pages_text)
    if total_chars == 0:
        return ConversionResult(False, SCANNED_PDF_MESSAGE, len(pages_text), 0, str(output))

    output.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    doc.add_heading(source.name, level=1)
    for index, text in enumerate(pages_text, start=1):
        if index > 1:
            doc.add_page_break()
        doc.add_heading(f"Page {index}", level=2)
        for block in text.splitlines():
            clean = block.strip()
            if clean:
                doc.add_paragraph(clean)
    doc.save(str(output))
    return ConversionResult(True, f"Converted PDF to simple text-only Word: {output}", len(pages_text), total_chars, str(output))


def _validate_paths(source: Path, output: Path) -> str:
    if not source.exists():
        return f"PDF file not found: {source}"
    if source.suffix.lower() != ".pdf":
        return "Please select a PDF file."
    if output.suffix and output.suffix.lower() != ".docx":
        return "Please choose a Word .docx output path."
    return ""


def _docx_path(path: str | Path, source: Path | None = None) -> Path:
    raw = str(path).strip()
    default_name = f"{source.stem}.docx" if source else "converted.docx"
    if not raw:
        return Path.cwd() / "output" / default_name

    output = Path(raw)
    if output.exists() and output.is_dir():
        return output / default_name
    if raw.endswith(("\\", "/")):
        return output / default_name
    if not output.suffix:
        output = output.with_suffix(".docx")
    return output


def get_ocr_availability() -> tuple[bool, str]:
    try:
        import pytesseract
    except Exception as exc:
        return False, f"{OCR_NOT_ENABLED_MESSAGE} Python OCR wrapper is unavailable. Details: {exc}"

    executable_path = configure_tesseract(pytesseract)
    if executable_path and _required_tessdata_available(executable_path):
        return True, f"Bundled OCR engine detected: {executable_path}"
    return (
        False,
        f"{OCR_NOT_ENABLED_MESSAGE} Tesseract OCR is not bundled with this portable build and was not found on this computer.",
    )


def configure_tesseract(pytesseract_module=None) -> Path | None:
    executable_path = find_tesseract_executable()
    if not executable_path:
        return None
    if pytesseract_module is not None:
        pytesseract_module.pytesseract.tesseract_cmd = str(executable_path)
    os.environ["TESSDATA_PREFIX"] = str(executable_path.parent / "tessdata")
    return executable_path


def find_tesseract_executable() -> Path | None:
    candidates = [
        _runtime_root() / "resources" / "ocr" / "tesseract" / "tesseract.exe",
        _project_root() / "resources" / "ocr" / "tesseract" / "tesseract.exe",
    ]
    bundled = getattr(sys, "_MEIPASS", None)
    if bundled:
        candidates.append(Path(bundled) / "resources" / "ocr" / "tesseract" / "tesseract.exe")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    system = shutil.which("tesseract")
    return Path(system) if system else None


def _required_tessdata_available(executable_path: Path) -> bool:
    tessdata = executable_path.parent / "tessdata"
    return (tessdata / "eng.traineddata").exists()


def _runtime_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return _project_root()


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _normalize_ocr_language(label: str) -> str:
    return {
        "English": "eng",
        "Simplified Chinese": "chi_sim",
        "Traditional Chinese": "chi_tra",
        "English + Simplified Chinese": "eng+chi_sim",
        "English + Traditional Chinese": "eng+chi_tra",
        "eng": "eng",
        "chi_sim": "chi_sim",
        "chi_tra": "chi_tra",
        "eng+chi_sim": "eng+chi_sim",
        "eng+chi_tra": "eng+chi_tra",
    }.get(label, "eng")


def _normalize_mode(mode: str) -> str:
    if mode in {MODE_EDITABLE, "editable", "layout", "layout_preserving"}:
        return MODE_EDITABLE
    if mode in {MODE_OCR, "ocr", "ocr_pdf"}:
        return MODE_OCR
    if mode in {MODE_SIMPLE, "simple", "simple_text"}:
        return MODE_SIMPLE
    if mode in {MODE_PPTX, "pptx", "pdf_to_pptx"}:
        return MODE_PPTX
    return MODE_EDITABLE


def _pdf_text_stats(source: Path) -> tuple[int, int, str]:
    pages_text, error = _extract_page_text(source, "1-end")
    return len(pages_text), sum(len(text) for text in pages_text), error


def _extract_page_text(source: Path, page_ranges: str = "1-end") -> tuple[list[str], str]:
    try:
        reader = PdfReader(str(source))
        if reader.is_encrypted:
            return [], "Could not open PDF. It may be encrypted or password protected."
        selected_pages, range_error = _selected_pages(page_ranges, len(reader.pages))
        if range_error:
            return [], range_error
        return [(reader.pages[page - 1].extract_text() or "").strip() for page in selected_pages], ""
    except Exception as exc:
        return [], f"Could not extract text from PDF. Details: {exc}"


def _selected_pages(page_ranges: str, page_count: int) -> tuple[list[int], str]:
    try:
        ranges = parse_page_ranges(page_ranges or "1-end", page_count)
    except Exception as exc:
        return [], f"Invalid page range: {exc}"
    pages: list[int] = []
    for page_range in ranges:
        pages.extend(range(page_range.start, page_range.end + 1))
    return pages, ""


def _selected_char_count(source: Path, selected_pages: list[int]) -> int:
    pages_text, _ = _extract_page_text(source, ",".join(str(page) for page in selected_pages))
    return sum(len(text) for text in pages_text)
