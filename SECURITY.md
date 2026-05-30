# Security Policy

## Supported Version

The current supported version is:

```text
Wallace's PDFirst 1.0 Portable
```

## Reporting a Security Issue

Please report security issues privately to the repository owner through GitHub if private vulnerability reporting is enabled, or by opening a minimal issue that does not expose sensitive exploit details.

Include:

- App version.
- Windows version.
- Steps to reproduce.
- Expected result.
- Actual result.
- Whether a sample file can be shared safely.

## Security and Privacy Design

- Core workflows process files locally.
- The app should not upload documents to external services by default.
- Portable builds should not require administrator rights.
- Settings should not store secrets in plain text.
- Future optional API features must be explicitly enabled by the user.

## Sensitive File Notice

Users should avoid sharing confidential, legal, academic, examination, governance, compliance, medical, financial, or personal documents in public issues.

