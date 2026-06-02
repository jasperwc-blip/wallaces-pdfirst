from __future__ import annotations

import sys


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--pdf2docx-worker":
        from app.pdf2docx_worker import main as worker_main

        return worker_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == "--pdf-ocr-worker":
        from app.services.pdf_to_word import MODE_OCR, convert_pdf_to_docx

        if len(sys.argv) < 4:
            print("Usage: --pdf-ocr-worker input.pdf output.docx [page-ranges] [language]")
            return 2
        page_ranges = sys.argv[4] if len(sys.argv) > 4 else "1-end"
        language = sys.argv[5] if len(sys.argv) > 5 else "English"
        result = convert_pdf_to_docx(sys.argv[2], sys.argv[3], MODE_OCR, page_ranges, language)
        print(result.message)
        return 0 if result.success else 1

    try:
        from PySide6.QtWidgets import QApplication, QStyleFactory
        from PySide6.QtGui import QFont
        from app.ui.main_window import MainWindow
    except Exception as exc:  # pragma: no cover - packaging guard
        print("Wallace's PDFirst requires bundled GUI dependencies.")
        print(f"Startup error: {exc}")
        return 2

    app = QApplication(sys.argv)
    app.setApplicationName("Wallace's PDFirst")
    app.setApplicationDisplayName("Wallace's PDFirst")
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setFont(QFont(_ui_font_family(), 9))
    app.setPalette(_light_palette())
    window = MainWindow()
    window.resize(1220, 760)
    window.show()
    return app.exec()


def _light_palette() -> "QPalette":
    from PySide6.QtGui import QColor, QPalette

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#f6f7f9"))
    palette.setColor(QPalette.WindowText, QColor("#111827"))
    palette.setColor(QPalette.Base, QColor("#ffffff"))
    palette.setColor(QPalette.AlternateBase, QColor("#f3f4f6"))
    palette.setColor(QPalette.Text, QColor("#111827"))
    palette.setColor(QPalette.Button, QColor("#ffffff"))
    palette.setColor(QPalette.ButtonText, QColor("#111827"))
    palette.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
    palette.setColor(QPalette.ToolTipText, QColor("#111827"))
    palette.setColor(QPalette.PlaceholderText, QColor("#6b7280"))
    palette.setColor(QPalette.Highlight, QColor("#bfdbfe"))
    palette.setColor(QPalette.HighlightedText, QColor("#111827"))
    return palette


def _ui_font_family() -> str:
    if sys.platform == "darwin":
        return ".AppleSystemUIFont"
    return "Segoe UI"


if __name__ == "__main__":
    raise SystemExit(main())
