# Changelog

## 1.0.0 Portable

Initial portable Windows release of Wallace's PDFirst.

### Added

- Split PDF by custom ranges, single-page burst, even pages, or odd pages.
- Merge PDF files with reorderable file list.
- Convert JPG/PNG images to PDF with reorderable file list.
- Rotate PDF pages clockwise by 90, 180, or 270 degrees.
- Convert VTT/SRT/TXT transcripts to DOCX or PDF.
- Add text or image watermarks with text formatting, position, transparency, and clockwise rotation controls.
- Per-feature session status logs.
- English, Traditional Chinese, and Simplified Chinese translation resources.
- Portable Windows build script using PyInstaller.
- Automated workflow tests that generate temporary test files at runtime.
- About page.

### Known Limitations

- OCR is not bundled in the default portable build.
- Settings are session-level in this version.
- Very large PDFs may require more processing time and memory.
