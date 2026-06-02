# Testing

## Run Unit Tests

```bat
.venv-build\Scripts\python -m unittest discover -s app\tests
```

The tests create temporary PDFs, images, transcript files, DOCX files, and PPTX files at runtime. No sample user files are required or bundled.

## Covered Workflows

- Page range parser.
- Image to PDF.
- Image-to-PDF orientation.
- Transcript parsing.
- Transcript to DOCX.
- Transcript to PDF.
- PDF to Word editable layout mode.
- PDF to Word simple text mode.
- PDF to Word OCR mode for scanned/image-only PDFs.
- PDF to PPTX validity and visual-layout background check.
- PDF merge.
- PDF split.
- Burst/even/odd split modes.
- PDF rotation.
- Text watermark.
- Image watermark.
- Sidebar order and About version.
- OCR mode availability in the release build.

Some internal service tests remain for legacy worksheet/marking helpers, but those workflows are not exposed in the current UI.

## Manual Smoke Test

1. Build with `build_portable_v1.0.1.bat`.
2. Open `dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe`.
3. Confirm the app title is Wallace's PDFirst.
4. Confirm sidebar modules:
   - Split PDF
   - Merge PDF
   - Rotate PDF
   - PDF to Word/PPT
   - Transcript to Word/PDF
   - Image to PDF
   - Add Watermark
   - Settings
   - About
5. Use your own non-confidential test PDFs/images/transcripts to run each workflow.
6. Test `OCR PDF` with a scanned/image-only PDF.
7. Confirm each feature status log shows progress and resets after restart.
8. Confirm no private files or generated output files are bundled in the release folder.
