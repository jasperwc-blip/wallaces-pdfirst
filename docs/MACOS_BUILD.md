# macOS Build and Release Notes

This repository currently documents Wallace's PDFirst v1.0.1 as a release-ready Windows portable app. A separate macOS build lane may be maintained later, but it must remain independent from the Windows portable release.

## Windows Release Must Not Be Modified

The Windows release output is:

```text
dist\Wallace's_PDFirst_v1.0.1\Wallaces_PDFirst.exe
```

Any future macOS build work must not rename, delete, overwrite, or restructure this Windows release folder.

## macOS Build Host Requirement

macOS `.app` bundles must be built on macOS. PyInstaller cannot produce a real macOS `.app` from Windows.

If a macOS lane is revived, keep macOS-specific files under `macos/` and build on a Mac.

## Suggested Future macOS Success Criteria

A macOS release is successful only when:

- macOS-specific files live separately under `macos/`.
- The same core Python services are reused where practical.
- Tests pass before packaging.
- The `.app` launches on macOS without requiring users to install Python.
- The Windows v1.0.1 portable release folder remains unchanged.
- No private samples or user files are bundled.
- Signing/notarization status is clearly stated.

## Future Release Naming

If macOS release assets are added later, use version-aligned naming:

```text
Wallaces-PDFirst-v1.0.1-macOS-Portable.zip
```

Do not upload macOS assets until they are built and verified on macOS.
