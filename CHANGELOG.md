# Changelog

## 1.0.1 Portable

Release-ready Windows portable build of Wallace's PDFirst.

### Added

- PDF to Word/PPT workflow.
- Editable layout-preserving PDF-to-Word mode.
- OCR PDF mode in the standard Windows portable folder.
- PDF-to-PPTX conversion with visual layout preservation and selectable text layer where practical.
- Bundled OCR runtime for English, Simplified Chinese, and Traditional Chinese in the standard v1.0.1 folder.
- Language-only Settings page with English, Simplified Chinese, and Traditional Chinese options.
- Dedicated v1.0.1 build script for the release-ready portable folder.

### Fixed

- PDF-to-PPTX layout handling so the rendered PDF page remains the top visual layer.
- OCR configuration for bundled Tesseract, including `TESSDATA_PREFIX`.
- Portable folder size by removing duplicate resources and pruning unused OCR training/language files.

### Verified

- Automated tests pass.
- Normal OCR build launches.
- Packaged OCR worker converts a scanned/image-only PDF into Word text.
- Existing v1.0.0 output folder remains untouched.

### Known Limitations

- OCR quality depends on source scan quality and selected language.
- PDF-to-PPTX prioritizes visual layout fidelity; complex PDF objects are not fully rebuilt as native editable PowerPoint charts/shapes.
- Settings are session-level in this version.

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
