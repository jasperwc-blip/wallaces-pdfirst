from __future__ import annotations

import sys


def main() -> int:
    try:
        from PySide6.QtWidgets import QApplication, QStyleFactory
        from PySide6.QtGui import QColor, QFont, QPalette
        from app.ui.main_window import MainWindow
    except Exception as exc:  # pragma: no cover - packaging guard
        print("Wallace's PDFirst requires bundled GUI dependencies.")
        print(f"Startup error: {exc}")
        return 2

    app = QApplication(sys.argv)
    app.setApplicationName("Wallace's PDFirst")
    app.setApplicationDisplayName("Wallace's PDFirst")
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setFont(QFont("Segoe UI", 9))
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


if __name__ == "__main__":
    raise SystemExit(main())
