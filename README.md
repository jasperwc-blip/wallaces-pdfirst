# Wallace's PDFirst

Wallace's PDFirst is a portable Windows desktop app for practical document workflows: PDF splitting, merging, rotation, layout-preserving PDF-to-Word/PPT conversion, image-to-PDF conversion, transcript conversion, and watermarking.

The Windows release opens directly from an `.exe` file. End users do not need Python, administrator rights, an installer, registry changes, or system-level dependency installation.

## Current Release

Current release-ready version:

```text
Wallace's PDFirst v1.0.1 Portable
```

Release portable output:

```text
dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe
```

This is the release-ready Windows portable folder. It includes bundled OCR support for English, Simplified Chinese, and Traditional Chinese.

## Features

- Split PDFs by custom ranges, burst single pages, even pages, or odd pages.
- Merge PDFs with user-controlled file order.
- Rotate selected PDF pages clockwise.
- Convert PDFs to Word DOCX locally with editable layout-preserving, OCR PDF, or simple text-only modes.
- Convert PDF pages to PPTX with preserved visual layout and a selectable text layer where practical.
- Convert VTT/SRT/TXT transcripts to DOCX or PDF.
- Convert JPG/PNG images to PDF with user-controlled file order.
- Add text or image watermarks with font, style, position, transparency, rotation, and page controls.
- Per-feature status logs that reset when the app closes.
- Settings and About pages.

## Run on Windows

Open the executable from the release portable folder:

```text
dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe
```

Distribute the whole `Wallace's_PDFirst_v1.0.1` folder, not only the `.exe`.

## Build on Windows

On Windows with Python 3.11 or 3.12:

```bat
build_portable_v1.0.1.bat
```

The build script creates/verifies the build virtual environment, installs dependencies, runs tests, builds with PyInstaller, prunes unnecessary OCR files, and creates the v1.0.1 portable folder.

Legacy build scripts are retained for history, but v1.0.1 release packaging should use `build_portable_v1.0.1.bat`.

## Test

```bat
.venv-build\Scripts\python -m unittest discover -s app\tests
```

Tests create temporary input files at runtime. No private user files are required.

## Documentation

- [GitHub repository steps](GITHUB_REPO_STEPS.md)
- [Build guide](docs/BUILD.md)
- [Release guide](docs/RELEASE.md)
- [User guide](docs/USER_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Testing](docs/TESTING.md)
- [Privacy notice](docs/PRIVACY.md)
- [Disclaimer](docs/DISCLAIMER.md)
- [Dependencies](docs/DEPENDENCIES.md)
- [Roadmap](docs/ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE.md)

## Privacy

Core workflows are local-first. The app does not upload documents to external services.

## Safety

Users should only process files they own, created, or are legally authorized to modify. Wallace's PDFirst must not be used to remove copyright notices, ownership marks, third-party attribution, anti-piracy marks, or other protected identifiers without proper authorization.

## Known Limitations

- Settings are session-level in this version.
- OCR quality depends on scan quality, page angle, language selection, and source image clarity.
- PDF-to-PPT prioritizes visual layout fidelity. Complex PDF charts, tables, and vector shapes are preserved visually, but are not fully reconstructed as native editable PowerPoint charts/shapes.
- Very large PDFs may take time and memory.

## Troubleshooting

- If output fails, choose a writable output folder and close the target PDF/DOCX/PPTX in other apps.
- Encrypted PDFs may fail unless they can be opened without a password.
- Use the release-ready `Wallace's_PDFirst_v1.0.1` folder for public distribution.
- If running from source fails, install dependencies with `pip install -r requirements.txt`.
