# Build Guide

## Requirements

- Windows 10 or Windows 11.
- Python 3.11 or 3.12 for development/building.
- Internet access during first dependency installation.

End users of the portable build do not need Python installed.

## Build Command

```bat
build_portable.bat
```

The script:

1. Cleans `build` and `dist`.
2. Creates or verifies `.venv-build`.
3. Installs dependencies from `requirements.txt`.
4. Runs automated tests.
5. Builds the app with PyInstaller.
6. Copies README, resources, and third-party notices.

## Output

```text
dist\Wallace's PDFirst\Wallace's PDFirst.exe
```

Distribute the entire `dist\Wallace's PDFirst` folder.

## Build Notes

PyInstaller uses the internal safe name `Wallaces_PDFirst`, then the build script renames the output folder and executable to `Wallace's PDFirst`.

This avoids quoting problems caused by the apostrophe in the public app name.

## Clean Build

```bat
rmdir /s /q build
rmdir /s /q dist
build_portable.bat
```

## Font and Interface Compatibility

The app sets Windows-safe UI fallbacks:

- Segoe UI
- Microsoft JhengHei UI
- Microsoft YaHei UI
- Arial

These fonts are broadly available on Windows and support English, Traditional Chinese, and Simplified Chinese labels.
