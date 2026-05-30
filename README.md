# Wallace's PDFirst

Wallace's PDFirst is a portable Windows desktop app for practical document workflows: PDF splitting, PDF merging, PDF rotation, image-to-PDF conversion, transcript conversion, and watermarking.

It opens directly from an `.exe` file. End users do not need an installer, administrator rights, registry changes, Python, or system-level dependency installation.

## Features

- Split PDFs by custom ranges, burst single pages, even pages, or odd pages.
- Merge PDFs with user-controlled file order.
- Convert JPG/PNG images to PDF with user-controlled file order.
- Rotate selected PDF pages clockwise.
- Convert VTT/SRT/TXT transcripts to DOCX or PDF.
- Add text or image watermarks with font, style, position, transparency, rotation, and page controls.
- Per-feature status logs that reset when the app closes.
- Settings and About pages.

## Run

After building, open:

```text
dist\Wallace's PDFirst\Wallace's PDFirst.exe
```

Distribute the whole `dist\Wallace's PDFirst` folder, not only the `.exe`.

## Build

On Windows with Python 3.11 or 3.12:

```bat
build_portable.bat
```

The build script creates/verifies the build virtual environment, installs dependencies, runs tests, builds with PyInstaller, and creates:

```text
dist\Wallace's PDFirst\Wallace's PDFirst.exe
```

No sample or private user files are bundled in the portable release.

## Test

```bat
python -m unittest discover -s app\tests
```

Tests create temporary input files at runtime.

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
- OCR is not bundled.
- Very large PDFs may take time and memory.

## Troubleshooting

- If output fails, choose a writable output folder and close the target PDF in other apps.
- Encrypted PDFs may fail unless they can be opened without a password.
- If running from source fails, install dependencies with `pip install -r requirements.txt`.
