# Architecture

Wallace's PDFirst is a Python/PySide6 portable Windows desktop app with document-processing services kept separate from the UI.

## Main Structure

```text
app/
  main.py
  ui/
    main_window.py
    i18n.py
  core/
    page_ranges.py
  services/
    pdf_ops.py
    pdf_to_word.py
    pdf_to_pptx.py
    transcript.py
  tests/
resources/
docs/
build_portable_v1.0.1.bat
requirements.txt
```

The current release-ready public UI exposes PDF split, merge, rotate, PDF to Word/PPT, transcript conversion, image-to-PDF, watermarking, Settings, and About.

## Design

- `app/main.py` is the application entry point and contains hidden worker commands used for packaged verification.
- `app/ui` contains the PySide6 desktop interface.
- `app/services` contains testable document-processing functions.
- `app/core` contains shared parsing utilities.
- `resources` contains translation files and bundled OCR runtime/data.
- `build_portable_v1.0.1.bat` builds the Windows v1.0.1 portable release folder.
- Tests create temporary files at runtime.

## Windows Outputs

```text
dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe
```

This release folder includes OCR support for English, Simplified Chinese, and Traditional Chinese.

## Core Libraries

- PySide6: desktop UI.
- PyMuPDF: PDF rendering, page images, text extraction, and PDF-to-PPT visual rendering.
- pdf2docx: editable layout-preserving PDF-to-Word conversion.
- pytesseract / bundled Tesseract: OCR PDF mode.
- python-pptx: PPTX output.
- pypdf: PDF merge, split, rotation, and page manipulation.
- Pillow: image processing.
- python-docx: Word output.
- reportlab: generated PDFs and watermark overlays.
- PyInstaller: portable Windows folder packaging.

## Local-First Processing

Core file processing runs locally. No document upload is performed by default.

## UI Flow

Most workflow pages follow this pattern:

1. File drop/input list.
2. Options panel.
3. Output selector.
4. Progress bar.
5. Run button.
6. Per-feature session status log.

Settings and About use dedicated pages rather than file-processing workflow controls.
