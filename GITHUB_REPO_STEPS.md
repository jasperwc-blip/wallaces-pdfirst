# GitHub Repository Steps for Wallace's PDFirst

This document describes what a senior Windows desktop application engineer and product architect should do to create, publish, release, and maintain the GitHub repository for Wallace's PDFirst.

Reference repository provided by Wallace:

```text
https://github.com/jasperwc-blip/notebook-converter
```

Use that repository only as a general reference for GitHub presentation and project hygiene. Wallace's PDFirst should have its own product-specific repository, release notes, safety notices, and portable-app build instructions.

## 1. Define Success Criteria

Before touching GitHub, define the release success criteria:

- The repository clearly explains what Wallace's PDFirst does.
- The repository contains source code, tests, build scripts, and documentation.
- The repository does not contain private PDFs, samples supplied by the user, generated output files, build folders, virtual environments, or release zip files.
- The Windows v1.0.1 portable app is built from source using `build_portable_v1.0.1.bat`.
- The release provides one downloadable Windows portable folder as the GitHub Release asset:
  - `Wallaces-PDFirst-v1.0.1-Windows-Portable.zip`
- Any local `Excl_OCR` build is ignored for this public release.
- The existing GitHub repository currently used for v1.0.0 is updated without deleting the v1.0.0 release or rewriting public history.
- The v1.0.1 release is published as a new GitHub Release tag, not as a replacement for the v1.0.0 release.
- The README lets a third-party user understand the app, run it, build it, and evaluate privacy/safety within one minute.

## 2. Confirm Product Scope

Product name:

```text
Wallace's PDFirst
```

Repository name:

```text
wallaces-pdfirst
```

Current release-ready version:

```text
v1.0.1 Portable
```

Main workflows:

- Split PDF.
- Merge PDF.
- Rotate PDF.
- PDF to Word/PPT.
- Transcript to Word/PDF.
- Image to PDF.
- Add Watermark.
- Settings.
- About.

Privacy posture:

- Local-first document processing.
- No document upload by default.
- No API key required for core functions.

Packaging posture:

- Portable Windows folder app.
- No installer.
- No administrator rights.
- No system-level dependency installation for end users.

## 3. Create the GitHub Repository

Skip this section if the repository already exists. Wallace currently uses:

```text
https://github.com/jasperwc-blip/wallaces-pdfirst
```

For updating the existing repository from v1.0.0 to v1.0.1, use the dedicated update checklist in Section 4A, then use the later sections as supporting reference.

On GitHub:

1. Sign in.
2. Click **New repository**.
3. Owner: `jasperwc-blip` or the intended account/organization.
4. Repository name: `wallaces-pdfirst`.
5. Description:

```text
Portable Windows desktop app for PDF splitting, merging, rotation, PDF-to-Word/PPT, image-to-PDF, transcript conversion, and watermarking.
```

6. Visibility: Public when ready for third-party users.
7. Add README: Off, if this local project already has `README.md`.
8. Add `.gitignore`: Off, if this local project already has `.gitignore`.
9. Add license: choose only if finalized. This project currently includes MIT license files.

## 4A. Update the Existing v1.0.0 Repository to v1.0.1

Use this path when `jasperwc-blip/wallaces-pdfirst` already exists and currently represents v1.0.0.

Senior release objective:

- preserve the existing v1.0.0 GitHub release;
- publish v1.0.1 as a new release;
- commit source/documentation updates for v1.0.1;
- upload only the OCR-enabled v1.0.1 Windows portable zip;
- ignore `Wallace's_PDFirst_v1.0.1_(Excl_OCR)`.

Step-by-step workflow:

1. Open the local project folder:

```bat
cd C:\Users\Wallace\Documents\Codex\2026-05-30\you-are-a-senior-windows-desktop
```

2. Confirm the remote points to the existing GitHub repository:

```bat
git remote -v
```

Expected remote:

```text
https://github.com/jasperwc-blip/wallaces-pdfirst.git
```

3. Pull the latest `main` before preparing the release:

```bat
git pull origin main
```

If Git reports unrelated histories or conflicts, stop and resolve carefully. Do not force-push over the public repository.

4. Confirm the current local release folder exists:

```bat
dir "dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe"
```

5. Run automated tests:

```bat
.venv-build\Scripts\python -m unittest discover -s app\tests
```

6. Rebuild only if needed:

```bat
build_portable_v1.0.1.bat
```

7. Verify the public release folder:

```bat
dir "dist\Wallace's_PDFirst_v1.0.1"
```

Do not use this folder for the public release:

```text
dist\Wallace's_PDFirst_v1.0.1_(Excl_OCR)
```

8. Confirm `.gitignore` excludes generated outputs:

```bat
git status --short
```

The following should not be staged:

```text
dist/
build/
build-v1.0.1/
.venv-build/
output/
*.zip
private PDFs, DOCX files, PPTX files, or screenshots
```

9. Stage source, resources, tests, build scripts, GitHub metadata, and documentation only:

```bat
git add .gitignore
git add README.md CHANGELOG.md LICENSE LICENSE.md SECURITY.md CONTRIBUTING.md CODE_OF_CONDUCT.md
git add GITHUB_REPO_STEPS.md requirements.txt build_portable_v1.0.1.bat
git add app resources docs .github
```

10. Review before committing:

```bat
git status
git diff --cached --stat
```

Confirm no private samples, generated output, release zip, or `dist` contents are staged.

11. Commit:

```bat
git commit -m "Update Wallace's PDFirst for v1.0.1"
```

12. Push:

```bat
git push origin main
```

13. Create the release ZIP from the OCR-enabled folder:

```powershell
Compress-Archive -Path "dist\Wallace's_PDFirst_v1.0.1" -DestinationPath "Wallaces-PDFirst-v1.0.1-Windows-Portable.zip" -Force
```

14. Extract the zip to a clean temporary folder and double-click:

```text
Wallaces_PDFirst.exe
```

Minimum public-release smoke test:

- app launches without installation;
- About shows `Version: 1.0.1 Portable`;
- PDF to Word/PPT page opens;
- OCR PDF mode appears in the normal public build;
- PDF to PPTX output opens in PowerPoint without repair prompts where practical;
- Split, Merge, Rotate, Image to PDF, Transcript, and Add Watermark screens open.

15. Draft a new GitHub Release:

```text
Tag: v1.0.1
Target: main
Title: Wallace's PDFirst v1.0.1 Portable
Asset: Wallaces-PDFirst-v1.0.1-Windows-Portable.zip
```

16. Paste the release notes from Section 16 or `docs/RELEASE.md`.

17. Publish the release only after the asset finishes uploading.

18. Download the published asset from GitHub, extract it on another Windows machine if available, and perform the same smoke test.

Release architecture rule:

- Git stores the source and documentation.
- GitHub Releases store the portable zip.
- Public v1.0.0 release history remains available.
- Public v1.0.1 is a new release tag and asset.

## 4. Prepare the Local Project Folder

Use the working directory:

```bat
cd C:\Users\Wallace\Documents\Codex\2026-05-30\you-are-a-senior-windows-desktop
```

Confirm source and documentation exist:

```bat
dir app
dir resources
dir docs
dir .github
dir build_portable_v1.0.1.bat
dir requirements.txt
dir README.md
dir CHANGELOG.md
dir LICENSE
dir LICENSE.md
dir SECURITY.md
dir CONTRIBUTING.md
dir CODE_OF_CONDUCT.md
```

Confirm the release folder exists as a local build output:

```bat
dir "dist\Wallace's_PDFirst_v1.0.1"
```

Do not commit `dist`.

## 5. Confirm `.gitignore`

The repository should ignore generated and private files:

```text
.venv-build/
.venv-macos-build/
build/
build-v1.0.1/
build-v1.0.2/
build-macos/
dist/
dist-macos/
output/
samples/
__pycache__/
*.pyc
*.log
*.zip
*.pdf
*.docx
*.pptx
```

Important nuance: if the repository intentionally includes non-private fixture files later, use a dedicated `tests/fixtures` allowlist and keep the files small and non-confidential.

## 6. Validate Before Commit

Run tests:

```bat
.venv-build\Scripts\python -m unittest discover -s app\tests
```

Build the release folders:

```bat
build_portable_v1.0.1.bat
```

Verify output:

```text
dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe
```

Manual checks:

- The executable launches by double-click.
- The release build shows `OCR PDF` in `PDF to Word/PPT`.
- The release build converts a scanned test PDF to DOCX.
- PDF-to-PPTX output opens without repair prompts.
- Sidebar order is correct.
- Settings and About open.
- No private samples or generated files are inside the release folder.

## 7. Initialize Git Locally

If the folder is not already a Git repository:

```bat
git init
git branch -M main
```

Check status:

```bat
git status
```

If Git reports dubious ownership on Windows, add the safe directory only for this project:

```bat
git config --global --add safe.directory C:/Users/Wallace/Documents/Codex/2026-05-30/you-are-a-senior-windows-desktop
```

## 8. Connect the Remote

For the Wallace's PDFirst repository:

```bat
git remote add origin https://github.com/jasperwc-blip/wallaces-pdfirst.git
```

If a remote already exists:

```bat
git remote set-url origin https://github.com/jasperwc-blip/wallaces-pdfirst.git
```

Verify:

```bat
git remote -v
```

## 9. Stage Only Repository Files

Stage source, build scripts, docs, resources, and GitHub metadata:

```bat
git add .gitignore
git add README.md CHANGELOG.md LICENSE LICENSE.md SECURITY.md CONTRIBUTING.md CODE_OF_CONDUCT.md
git add GITHUB_REPO_STEPS.md requirements.txt build_portable.bat build_portable_v1.0.1.bat
git add app resources docs .github
```

Do not stage:

```text
dist/
dist-macos/
build/
build-v1.0.1/
build-v1.0.2/
.venv-build/
output/
private documents
generated PDFs
generated DOCX files
generated PPTX files
release ZIP files
```

Review:

```bat
git status
```

## 10. Commit

Use a clear baseline commit:

```bat
git commit -m "Add Wallace's PDFirst v1.0.1 portable Windows app"
```

Good commit hygiene:

- no generated build artifacts;
- no private files;
- no confidential screenshots;
- docs match current release;
- tests included;
- build script included.

## 11. Push to GitHub

If the GitHub repository is empty:

```bat
git push -u origin main
```

If the GitHub repository already has an initial commit:

```bat
git pull origin main --allow-unrelated-histories
git status
```

Resolve conflicts carefully, then:

```bat
git push -u origin main
```

## 12. Configure Repository Settings

In GitHub settings:

1. Enable Issues.
2. Enable Discussions if you want user feedback.
3. Enable Releases.
4. Disable Wiki unless you will maintain it.
5. Enable branch protection for `main` when the project gains contributors.
6. Add topics:

```text
pdf
windows
portable-app
pyside6
python
desktop-app
document-conversion
ocr
pdf-to-word
pdf-to-ppt
watermark
local-first
```

7. Set About description to the short product description.
8. Add a project website later only if you create a maintained page.

## 13. Review Repository Presentation

A senior product repo should make trust obvious. Confirm:

- `README.md` explains what the app does, how to run it, how to build it, and limitations.
- `docs/BUILD.md` explains v1.0.1 build outputs.
- `docs/RELEASE.md` explains release packaging.
- `docs/TESTING.md` explains automated and manual tests.
- `docs/PRIVACY.md` explains local-first behavior.
- `docs/DISCLAIMER.md` explains legal/professional limitations.
- `SECURITY.md` explains how to report security issues.
- `CHANGELOG.md` includes v1.0.1.
- `LICENSE` / `LICENSE.md` are consistent.

## 14. Create Release ZIP Assets

Build first:

```bat
build_portable_v1.0.1.bat
```

Create the release ZIP file:

```powershell
Compress-Archive -Path "dist\Wallace's_PDFirst_v1.0.1" -DestinationPath "Wallaces-PDFirst-v1.0.1-Windows-Portable.zip" -Force
```

Before upload, verify the ZIP by extracting it to a clean folder and opening the `.exe`.

## 15. Create the GitHub Release

On GitHub:

1. Open **Releases**.
2. Click **Draft a new release**.
3. Tag: `v1.0.1`.
4. Target: `main`.
5. Release title:

```text
Wallace's PDFirst v1.0.1 Portable
```

6. Upload:

```text
Wallaces-PDFirst-v1.0.1-Windows-Portable.zip
```

7. Use release notes from `docs/RELEASE.md`.
8. Publish after confirming the assets finish uploading.

## 16. Suggested GitHub Release Notes

```text
Wallace's PDFirst v1.0.1 Portable

Portable Windows desktop release.

Asset:
- Windows Portable: includes OCR PDF support for English, Simplified Chinese, and Traditional Chinese.

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

Known limitations:
- OCR quality depends on scan quality and selected language.
- PDF-to-PPT prioritizes visual layout fidelity; complex PDF objects are not fully reconstructed as native PowerPoint charts/shapes.
- Settings are session-level.
```

## 17. Senior QA Before Public Announcement

Test the release folder on at least two Windows machines if possible:

- Windows 10.
- Windows 11.
- Display scaling: 100%, 125%, 150%.
- Light mode and dark mode.
- Non-admin user account.
- Folder path with spaces and apostrophe.
- Double-click launch.
- Split PDF.
- Merge PDF.
- Rotate PDF.
- PDF to Word editable mode.
- PDF to Word OCR mode.
- PDF to PPTX mode.
- Transcript to Word/PDF.
- Image to PDF.
- Add Watermark.
- Language selection in Settings.
- About page version.

Confirm:

- no installation is needed;
- no admin rights are requested;
- no documents are uploaded;
- no private files are bundled;
- generated output goes only to the selected output path.

## 18. Recommended GitHub Repository Creation Workflow

A senior Windows desktop application engineer and product architect should create and publish the repository in this order:

1. Finalize the product scope, version number, license, privacy posture, and public release target.
2. Confirm the app builds locally and the release-ready folder exists at `dist\Wallace's_PDFirst_v1.0.1`.
3. Run automated tests and a manual smoke test on the release `.exe`.
4. Remove or ignore generated files, private documents, output files, virtual environments, and release ZIPs from Git history.
5. Create the GitHub repository as `wallaces-pdfirst` under `jasperwc-blip`.
6. Use the short repository description from this document.
7. Keep GitHub's initial README and `.gitignore` options off if local files already exist.
8. Choose the finalized license, currently MIT in this repository.
9. Initialize Git locally, set branch `main`, connect the remote, and pull any initial GitHub commit if needed.
10. Stage only source code, resources, build scripts, tests, documentation, and GitHub metadata.
11. Commit with a clear baseline message.
12. Push to `main`.
13. Configure repository About text, topics, Issues, Releases, and basic security/contact settings.
14. Create a clean release ZIP from `dist\Wallace's_PDFirst_v1.0.1`.
15. Draft GitHub Release `v1.0.1`, upload the ZIP, paste release notes, and publish only after the asset upload completes.
16. Download the published ZIP on another Windows machine, extract it, double-click the `.exe`, and perform a final public-user smoke test.
17. After release, maintain future changes through branches and pull requests, with tests and documentation updates before merging.

## 19. Maintenance Workflow

For each future change:

```bat
git checkout -b feature/short-description
.venv-build\Scripts\python -m unittest discover -s app\tests
build_portable_v1.0.1.bat
git status
git add <changed files>
git commit -m "Describe the change"
git push -u origin feature/short-description
```

Then open a pull request.

Pull request checklist:

- Does the change preserve portable execution?
- Does it avoid admin rights and installation requirements?
- Are tests updated?
- Are docs updated?
- Does the UI remain readable across Windows themes and scaling?
- Are private/generated files excluded?
- Are privacy and safety implications documented?

## 20. Versioning

Use semantic versioning:

```text
v1.0.1
v1.0.2
v1.1.0
v2.0.0
```

Suggested meaning:

- Patch: bug fixes, UI display fixes, OCR/build packaging fixes.
- Minor: new workflow or meaningful feature improvement.
- Major: breaking workflow or packaging change.

## 21. What Not to Commit

Never commit:

- `dist/`
- `dist-macos/`
- `build/`
- `build-v1.0.1/`
- `.venv-build/`
- sample/private PDFs;
- user output files;
- API keys;
- logs;
- confidential screenshots;
- generated release ZIP files.

Release ZIP files belong on GitHub Releases, not in the Git history.

## 22. Final Senior Engineer Rule

The repository should let a third-party user answer three questions within one minute:

1. What does Wallace's PDFirst do?
2. How do I run or build it?
3. Can I trust how it handles my files?

If the README, release page, or folder structure does not answer those clearly, improve the documentation before announcing the project.
