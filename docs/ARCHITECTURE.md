# Architecture

Wallace's PDFirst is a Python/PySide6 portable Windows desktop app.

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
    transcript.py
  tests/
resources/
docs/
build_portable.bat
requirements.txt
```

Additional internal service modules may remain for future work, but the current public UI exposes PDF split/merge/rotate, image-to-PDF, transcript conversion, watermarking, Settings, and About.

## Design

- `app/ui` contains the PySide6 desktop interface.
- `app/services` contains testable document-processing functions.
- `app/core` contains shared parsing utilities.
- `resources` contains translation files.
- Tests create temporary files at runtime.

## Core Libraries

- PySide6: Windows desktop UI.
- pypdf: PDF merge, split, rotation, and page manipulation.
- Pillow: image processing.
- python-docx: Word output.
- reportlab: generated PDFs and watermark overlays.
- PyInstaller: portable Windows packaging.

## Local-First Processing

Core file processing runs locally. No document upload is performed by default.

## UI Flow

Each workflow page follows the same pattern:

1. File drop/input list.
2. Options panel.
3. Output selector.
4. Progress bar.
5. Run button.
6. Per-feature session status log.
