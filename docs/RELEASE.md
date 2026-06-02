# Release Guide

## Version

Current release:

```text
Wallace's PDFirst v1.0.1 Portable
```

## Pre-Release Checklist

- README is current.
- CHANGELOG is current.
- About page text is current.
- Tests pass.
- Portable build completes.
- The v1.0.1 release executable exists.
- The v1.0.1 release build launches.
- OCR build can convert a scanned/image-only PDF to DOCX.
- App launches by double-clicking the exe.
- Sidebar and labels render correctly on Windows display scaling at 100%, 125%, and 150%.
- No sample, private, generated, or user-provided files are included in the portable release folders.
- No generated build folders are committed to Git.
- Existing v1.0.0 output, if present, is not modified.
- Existing GitHub v1.0.0 release remains published and unchanged.
- v1.0.1 is published as a new GitHub Release tag.
- The public release asset uses the OCR-enabled `Wallace's_PDFirst_v1.0.1` folder.
- The local `Wallace's_PDFirst_v1.0.1_(Excl_OCR)` folder is not uploaded for this release.

## Windows Build

```bat
build_portable_v1.0.1.bat
```

## Windows Verify

Expected outputs:

```text
dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe
```

Manual checks:

- Open the release app.
- Run Split PDF on a non-confidential test PDF.
- Run Merge PDF on non-confidential test PDFs.
- Run Image to PDF on non-confidential test PNG/JPG files.
- Run Transcript to DOCX/PDF on a non-confidential VTT/SRT/TXT file.
- Run PDF to Word/PPT in editable Word mode.
- Run PDF to Word/PPT in PDF to PPTX mode.
- Run OCR PDF mode using a non-confidential scanned PDF.
- Add text watermark to a non-confidential test PDF.
- Confirm About page appears below Settings.
- Confirm no private samples or user output files are bundled.

## Windows Package

Create the release zip file from the portable folder:

```powershell
Compress-Archive -Path "dist\Wallace's_PDFirst_v1.0.1" -DestinationPath "Wallaces-PDFirst-v1.0.1-Windows-Portable.zip" -Force
```

Do not zip or upload:

```text
dist\Wallace's_PDFirst_v1.0.1_(Excl_OCR)
```

After creating the zip, extract it to a clean temporary folder and launch:

```text
Wallaces_PDFirst.exe
```

Confirm the extracted app opens without installation, administrator rights, Python, or system-level dependencies.

## GitHub v1.0.1 Release Update

Use this when updating the existing `jasperwc-blip/wallaces-pdfirst` repository from v1.0.0 to v1.0.1.

1. Confirm the local branch is up to date:

```bat
git pull origin main
```

2. Run tests:

```bat
.venv-build\Scripts\python -m unittest discover -s app\tests
```

3. Build or confirm the release folder:

```bat
build_portable_v1.0.1.bat
dir "dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe"
```

4. Stage and commit source/documentation changes only:

```bat
git add .gitignore README.md CHANGELOG.md GITHUB_REPO_STEPS.md requirements.txt build_portable_v1.0.1.bat app resources docs .github
git commit -m "Update Wallace's PDFirst for v1.0.1"
git push origin main
```

5. Create and verify the portable zip:

```powershell
Compress-Archive -Path "dist\Wallace's_PDFirst_v1.0.1" -DestinationPath "Wallaces-PDFirst-v1.0.1-Windows-Portable.zip" -Force
```

6. On GitHub, create a new release:

```text
Tag: v1.0.1
Target: main
Release title: Wallace's PDFirst v1.0.1 Portable
Asset: Wallaces-PDFirst-v1.0.1-Windows-Portable.zip
```

7. Paste the notes below, publish the release, then download the published asset and run a final smoke test.

## GitHub Release Notes

```text
Wallace's PDFirst v1.0.1 Portable

Release-ready portable Windows desktop build.

Asset:
- Wallaces-PDFirst-v1.0.1-Windows-Portable.zip

Features:
- Split PDF by custom ranges, burst pages, even pages, or odd pages.
- Merge PDFs with reorderable file list.
- Rotate PDF pages clockwise.
- Convert JPG/PNG images to PDF with reorderable file list.
- Convert VTT/SRT/TXT transcripts to DOCX or PDF.
- Convert PDFs to Word using editable layout-preserving, OCR PDF, or simple text modes.
- Convert PDF pages to PPTX with preserved visual layout and selectable text where practical.
- Add text/image watermarks with formatting, position, transparency, and rotation controls.
- Per-feature status logs.
- Settings and About pages.

Privacy:
- Core document processing is local-first.
- No documents are uploaded by default.
- No installer or administrator rights required.
- No sample/private user files are bundled.

Build notes:
- The v1.0.1 portable folder includes bundled OCR for English, Simplified Chinese, and Traditional Chinese.

Known limitations:
- OCR quality depends on scan quality and language selection.
- PDF-to-PPT prioritizes visual layout fidelity; complex PDF objects are not fully reconstructed as native PowerPoint charts/shapes.
- Settings are session-level.
```
