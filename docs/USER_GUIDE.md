# User Guide

## Start the App

Open one of the portable executables:

```text
Wallaces_PDFirst.exe
```

No installation is required.

Use the release-ready `Wallace's_PDFirst_v1.0.1` folder.

## Split PDF

1. Add or drag a PDF into the file area.
2. Choose a split option:
   - `custom_ranges`
   - `burst_single_pages`
   - `even_pages`
   - `odd_pages`
3. For custom ranges, enter values such as:

```text
1-1, 2-3, 4-end
```

4. Select an output folder.
5. Click Run.

## Merge PDF

1. Add multiple PDFs.
2. Reorder them by dragging, or use Move Up / Move Down.
3. Select the output PDF path.
4. Click Run.

## Rotate PDF

1. Add a PDF.
2. Choose clockwise angle: 90, 180, or 270.
3. Enter pages such as `1-end` or `1,3,5-7`.
4. Select the output PDF path.
5. Click Run.

## PDF to Word/PPT

1. Add one PDF.
2. Choose a conversion mode:
   - `Editable Word - layout-preserving`
   - `OCR PDF`
   - `Simple text`
   - `PDF to PPTX`
3. Enter pages such as `1-end`, `1-3`, or `2,4,6`.
4. For OCR mode, choose the OCR language.
5. Select the output `.docx` or `.pptx` path.
6. Click Run.

Notes:

- `OCR PDF` is included in the release-ready portable build.
- `PDF to PPTX` prioritizes visual layout fidelity and adds selectable text where practical.
- Complex PDF objects are preserved visually, but not fully rebuilt as native editable PowerPoint charts/shapes.

## Transcript to Word/PDF

1. Add a `.vtt`, `.srt`, or `.txt` transcript.
2. Choose DOCX or PDF output.
3. Choose timestamp/speaker/duplicate/grouping options.
4. Select the output path.
5. Click Run.

## Image to PDF

1. Add JPG or PNG images.
2. Reorder them by dragging, or use Move Up / Move Down.
3. Choose sizing, orientation, and margin.
4. Select the output PDF path.
5. Click Run.

## Add Watermark

1. Add a PDF.
2. Choose text or image watermark.
3. For text, set wording, font, size, style, color, position, transparency, rotation, and pages.
4. For image, choose the image path, position, transparency, and pages.
5. Select the output PDF path.
6. Click Run.

## Settings

Choose the display language:

- English
- Simplified Chinese
- Traditional Chinese

Settings are session-level in v1.0.1.

## Status Logs

Each feature has its own session status log. Logs reset when the app closes.
