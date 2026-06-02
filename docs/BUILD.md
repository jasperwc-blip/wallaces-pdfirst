# Build Guide

## Windows Requirements

- Windows 10 or Windows 11.
- Python 3.11 or 3.12 for development/building.
- Internet access during first dependency installation.

End users of the portable build do not need Python installed.

## Release Build Command

For Wallace's PDFirst v1.0.1:

```bat
build_portable_v1.0.1.bat
```

The script:

1. Cleans the v1.0.1 build and staging folders.
2. Creates or verifies `.venv-build`.
3. Installs dependencies from `requirements.txt`.
4. Runs automated tests.
5. Builds the app with PyInstaller.
6. Copies README and third-party notices.
7. Prunes unused OCR language/training files.
8. Creates the release-ready OCR-enabled portable folder.

## Windows Outputs

```text
dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe
```

Distribute the entire `Wallace's_PDFirst_v1.0.1` folder.

## OCR Build Difference

`Wallace's_PDFirst_v1.0.1` includes:

- bundled Tesseract OCR runtime;
- English OCR data;
- Simplified Chinese OCR data;
- Traditional Chinese OCR data.

The public v1.0.1 release uses the OCR-enabled folder. Any local `Excl_OCR` build is not part of the public release package.

## Clean Build

```bat
rmdir /s /q build-v1.0.1
rmdir /s /q "dist\Wallace's_PDFirst_v1.0.1"
build_portable_v1.0.1.bat
```

## Font and Interface Compatibility

The app sets platform-safe UI fallbacks.

On Windows:

- Segoe UI
- Microsoft JhengHei UI
- Microsoft YaHei UI
- Arial

These fonts are broadly available on Windows and support English, Traditional Chinese, and Simplified Chinese labels.

## Legacy and macOS Notes

`build_portable.bat` and `build_portable_v1.0.2.bat` may exist in the repository history, but the release-ready Windows v1.0.1 build is produced by `build_portable_v1.0.1.bat`.

macOS build notes are retained separately in `docs/MACOS_BUILD.md`. The current release-ready deliverable described here is the Windows portable v1.0.1 build.
