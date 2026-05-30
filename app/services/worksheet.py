from __future__ import annotations

from pathlib import Path

from app.services.pdf_ops import remove_pdf_annotations


def clean_worksheet_pdf(
    input_pdf: str | Path,
    output_pdf: str | Path,
    exception_words: list[str] | None = None,
    remove_annotations: bool = True,
) -> Path:
    """Clean safely removable answer layers while preserving page content.

    Current local-first implementation removes annotation answers. Baked-in
    typed/handwritten answers require manual rectangles or OCR/vision support.
    Exception words are accepted for UI/API compatibility and documented limits.
    """
    _ = exception_words or []
    if remove_annotations:
        return remove_pdf_annotations(input_pdf, output_pdf)
    raise ValueError("No worksheet cleaning mode was selected.")
