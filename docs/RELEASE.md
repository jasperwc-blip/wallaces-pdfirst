# Release Guide

## Version

Current release:

```text
1.0 Portable
```

## Pre-Release Checklist

- README is current.
- CHANGELOG is current.
- About page text is current.
- Tests pass.
- Portable build completes.
- App launches by double-clicking the exe.
- Sidebar and labels render correctly on Windows display scaling at 100%, 125%, and 150%.
- No sample, private, generated, or user-provided files are included in the portable folder.
- No generated build folders are committed.

## Build

```bat
build_portable.bat
```

## Verify

```text
dist\Wallace's PDFirst\Wallace's PDFirst.exe
```

Manual checks:

- Open app.
- Run Split PDF on a non-confidential test PDF.
- Run Merge PDF on non-confidential test PDFs.
- Run Image to PDF on non-confidential test PNG/JPG files.
- Run Transcript to DOCX/PDF on a non-confidential VTT/SRT/TXT file.
- Add text watermark to a non-confidential test PDF.
- Confirm About page appears below Settings.
- Confirm no `samples` folder exists in `dist\Wallace's PDFirst`.

## Package

```bat
powershell Compress-Archive -Path "dist\Wallace's PDFirst" -DestinationPath "Wallaces-PDFirst-v1.0-portable.zip" -Force
```

## GitHub Release Notes

```text
Wallace's PDFirst v1.0 Portable

Portable Windows desktop release.

Features:
- Split PDF by custom ranges, burst pages, even pages, or odd pages.
- Merge PDFs with reorderable file list.
- Convert JPG/PNG images to PDF with reorderable file list.
- Rotate PDF pages clockwise.
- Convert VTT/SRT/TXT transcripts to DOCX or PDF.
- Add text/image watermarks with formatting, position, transparency, and rotation controls.
- Per-feature status logs.
- Settings and About pages.

Privacy:
- Core document processing is local-first.
- No installer or administrator rights required.
- No sample/private user files are bundled.

Known limitations:
- OCR is not bundled.
- Settings are session-level.
```
