# Contributing

Thank you for considering a contribution to Wallace's PDFirst.

## Project Principles

- Keep the app portable: no installer, admin rights, registry changes, or system-level dependency installation for end users.
- Keep core processing local-first.
- Prefer simple, reviewable document workflows over opaque automation.
- Avoid features that enable unlawful removal of copyright, ownership, attribution, or anti-piracy markings.
- Keep UI changes practical and clear.

## Development Setup

```bat
py -3.12 -m venv .venv-build
.venv-build\Scripts\pip install -r requirements.txt
.venv-build\Scripts\python -m unittest discover -s app\tests
```

Run from source:

```bat
.venv-build\Scripts\python -m app.main
```

Build portable release:

```bat
build_portable.bat
```

## Pull Request Checklist

- Tests pass.
- Portable build completes on Windows.
- New user-facing labels are clear.
- README/docs are updated when behavior changes.
- No generated folders are committed.
- No samples, private documents, generated PDFs, or user files are committed.
- Legal/privacy limitations are documented for sensitive document editing features.

## Code Style

- Prefer small, testable service functions under `app/services`.
- Keep PySide6 UI code thin and call service functions.
- Keep errors user-friendly in the UI and specific in logs.
- Do not add external network processing unless it is explicitly optional and user-enabled.
