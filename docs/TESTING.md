# Testing

## Run Unit Tests

```bat
python -m unittest discover -s app\tests
```

The tests create temporary PDFs, images, and transcript files at runtime. No sample user files are required or bundled.

## Covered Workflows

- Page range parser.
- Image to PDF.
- Image-to-PDF orientation.
- Transcript parsing.
- Transcript to DOCX.
- Transcript to PDF.
- PDF merge.
- PDF split.
- Burst/even/odd split modes.
- PDF rotation.
- Text watermark.
- Image watermark.

Some internal service tests remain for legacy worksheet/marking helpers, but those workflows are not exposed in the current UI.

## Manual Smoke Test

1. Build with `build_portable.bat`.
2. Open `dist\Wallace's PDFirst\Wallace's PDFirst.exe`.
3. Confirm the app title is Wallace's PDFirst.
4. Confirm sidebar modules:
   - Split PDF
   - Merge PDF
   - Image to PDF
   - Rotate PDF
   - Transcript to Word/PDF
   - Add Watermark
   - Settings
   - About
5. Use your own non-confidential test PDFs/images/transcripts to run each workflow.
6. Confirm each feature status log shows progress and resets after restart.
