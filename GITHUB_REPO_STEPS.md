# GitHub Repository Steps for Wallace's PDFirst

This document describes, step by step, what a senior Windows desktop application engineer and product architect should do to create, publish, and maintain a GitHub repository for Wallace's PDFirst.

Reference repository provided by Wallace:

```text
https://github.com/jasperwc-blip/notebook-converter
```

Use that repository as a general reference for GitHub presentation and project hygiene, but create or adapt a repository specifically for Wallace's PDFirst.

## 1. Define the Repository Purpose

Before creating the repository, write down the product scope:

- Product name: Wallace's PDFirst.
- Product type: portable Windows desktop application.
- Main workflows: PDF split, merge, rotate, image-to-PDF, transcript conversion, watermarking.
- Packaging goal: portable folder containing `Wallace's PDFirst.exe` and bundled runtime resources.
- Privacy posture: local-first document processing.
- User profile: practical document users who need simple PDF and transcript workflows without installation.

This prevents the repository from becoming a mix of unrelated experiments, generated files, and private document samples.

## 2. Decide the Repository Name

Recommended repository name:

```text
wallaces-pdfirst
```

Alternative if reusing the provided GitHub account/repo pattern:

```text
pdfirst
wallaces-pdfirst-portable
```

Avoid names that imply affiliation with existing proprietary PDF products.

## 3. Create the GitHub Repository

On GitHub:

1. Sign in.
2. Click New repository.
3. Owner: choose the intended account or organization.
4. Repository name: `wallaces-pdfirst`.
5. Description:

```text
Portable Windows desktop app for PDF splitting, merging, rotation, image-to-PDF, transcript conversion, and watermarking.
```

6. Visibility: Public if you intend third-party use; Private if still preparing.
7. Do not add a GitHub README if this local project already has one.
8. Do not add a `.gitignore` if this local project already has one.
9. Add license only if you have finalized licensing. This project currently includes `LICENSE.md`.

## 4. Prepare the Local Project Folder

From this folder:

```bat
cd C:\Users\Wallace\Documents\Codex\2026-05-30\you-are-a-senior-windows-desktop
```

Confirm required source and documentation files:

```bat
dir app
dir resources
dir docs
dir build_portable.bat
dir requirements.txt
dir README.md
dir LICENSE.md
dir CHANGELOG.md
dir SECURITY.md
dir CONTRIBUTING.md
```

Confirm generated folders are not intended for Git:

```text
.venv-build
build
dist
__pycache__
```

Confirm private/user files are not present:

```text
samples
output
private PDFs
generated PDFs
generated DOCX files
screenshots containing confidential content
API keys or credentials
```

## 5. Confirm `.gitignore`

A senior Windows desktop repo should ignore:

- virtual environments;
- PyInstaller build output;
- Python cache files;
- local output folders;
- generated PDFs/images/docs;
- editor files;
- OS files.

Run:

```bat
type .gitignore
```

If needed, ensure these are covered:

```text
.venv-build/
build/
dist/
__pycache__/
*.pyc
output/
*.log
```

## 6. Validate the App Before First Commit

Run tests:

```bat
.venv-build\Scripts\python -m unittest discover -s app\tests
```

Run a build:

```bat
build_portable.bat
```

Open the built app:

```text
dist\Wallace's PDFirst\Wallace's PDFirst.exe
```

Manual checks:

- Sidebar labels are readable.
- Fonts display correctly on Windows.
- Split PDF page opens.
- Settings and About pages open.
- No sample folder is included in the portable release.

## 7. Initialize Git Locally

If this folder is not already a Git repo:

```bat
git init
git branch -M main
```

Check status:

```bat
git status
```

## 8. Connect the Remote

For a new Wallace's PDFirst repo:

```bat
git remote add origin https://github.com/<your-account>/wallaces-pdfirst.git
```

If you intentionally want to use the reference repository URL:

```bat
git remote add origin https://github.com/jasperwc-blip/notebook-converter.git
```

If a remote already exists and must be changed:

```bat
git remote set-url origin https://github.com/<your-account>/wallaces-pdfirst.git
```

Verify:

```bat
git remote -v
```

## 9. Stage Only Repository-Appropriate Files

Use explicit staging for the first commit:

```bat
git add .gitignore
git add README.md LICENSE.md CHANGELOG.md SECURITY.md CONTRIBUTING.md CODE_OF_CONDUCT.md
git add GITHUB_REPO_STEPS.md build_portable.bat requirements.txt
git add app resources docs
```

Do not stage:

```text
dist
build
.venv-build
samples
output
private documents
generated PDFs/images/DOCX files
```

Review before commit:

```bat
git status
```

## 10. Make the First Commit

```bat
git commit -m "Add Wallace's PDFirst portable Windows app"
```

Good commit principles:

- one product-ready baseline;
- no generated build artifacts;
- no private files;
- documentation included;
- build script included;
- tests included.

## 11. Push to GitHub

If the GitHub repo is empty:

```bat
git push -u origin main
```

If the GitHub repo already has files:

```bat
git pull origin main --allow-unrelated-histories
git status
```

Resolve conflicts carefully, then:

```bat
git push -u origin main
```

## 12. Configure the GitHub Repository

In GitHub repository settings:

1. Enable Issues.
2. Enable Discussions if you want product feedback.
3. Enable Releases.
4. Disable Wikis unless you plan to maintain one.
5. Add topics:

```text
pdf
windows
portable-app
pyside6
python
document-tools
transcript
watermark
desktop-app
```

6. Add the website field later if you create a project page.

## 13. Add Repository Presentation

A senior product repo should make trust obvious. Confirm these files are clear:

- `README.md`: what it is, features, build/run/test, privacy, limitations.
- `docs/USER_GUIDE.md`: user workflow instructions.
- `docs/BUILD.md`: developer build instructions.
- `docs/RELEASE.md`: packaging and release checklist.
- `docs/PRIVACY.md`: local-first privacy statement.
- `docs/DISCLAIMER.md`: legal/professional-use disclaimer.
- `SECURITY.md`: how to report security issues.
- `CHANGELOG.md`: release history.
- `LICENSE.md`: license/copyright position.

## 14. Create a Portable Release Package

Run:

```bat
build_portable.bat
```

Verify output:

```text
dist\Wallace's PDFirst\Wallace's PDFirst.exe
```

Confirm the release folder contains no sample folder:

```bat
dir "dist\Wallace's PDFirst"
```

Create a zip:

```bat
powershell Compress-Archive -Path "dist\Wallace's PDFirst" -DestinationPath "Wallaces-PDFirst-v1.0-portable.zip" -Force
```

## 15. Create the First GitHub Release

On GitHub:

1. Open Releases.
2. Click Draft a new release.
3. Tag: `v1.0.0`.
4. Target: `main`.
5. Title:

```text
Wallace's PDFirst v1.0 Portable
```

6. Upload:

```text
Wallaces-PDFirst-v1.0-portable.zip
```

7. Release notes:

```text
Initial portable Windows release.

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

8. Publish release.

## 16. Senior QA Checklist Before Public Announcement

Test on at least two Windows machines if possible:

- Windows 10, Windows 11.
- Display scaling: 100%, 125%, 150%.
- Light mode and dark mode.
- Non-admin user account.
- Folder path with spaces and apostrophe.
- Open app by double-click.
- Run each visible workflow with non-confidential test files.
- Confirm all text is readable.
- Confirm output files are created in user-selected folders.
- Confirm no network upload occurs.

## 17. Maintenance Workflow

For every new change:

```bat
git checkout -b feature/short-description
.venv-build\Scripts\python -m unittest discover -s app\tests
build_portable.bat
git status
git add <changed files>
git commit -m "Describe the change"
git push -u origin feature/short-description
```

Then open a pull request.

Pull request review checklist:

- Does the change preserve portable execution?
- Does it require admin rights or installation? If yes, reject or redesign.
- Are tests updated?
- Are docs updated?
- Does the UI remain readable across Windows themes?
- Are private/generated files excluded?
- Are legal/privacy risks documented?

## 18. Versioning

Use simple semantic versioning:

```text
v1.0.0
v1.0.1
v1.1.0
v2.0.0
```

Suggested meaning:

- Patch: bug fixes, UI display fixes, packaging fixes.
- Minor: new workflow or meaningful feature improvement.
- Major: breaking workflow or packaging change.

## 19. What Not to Commit

Never commit:

- `dist/`
- `build/`
- `.venv-build/`
- sample/private PDFs;
- user output files;
- API keys;
- logs;
- confidential screenshots;
- generated release zip files unless intentionally attached to GitHub Releases.

## 20. Final Senior Engineer Rule

The repository should let a third-party user answer three questions within one minute:

1. What does Wallace's PDFirst do?
2. How do I run or build it?
3. Can I trust how it handles my files?

If the README, release page, or folder structure does not answer those clearly, improve the documentation before announcing the project.
