from __future__ import annotations
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QPlainTextEdit,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.services.pdf_ops import (
    add_image_watermark,
    add_text_watermark,
    image_files_to_pdf,
    merge_pdfs,
    rotate_pdf,
    split_pdf_by_mode,
)
from app.services.transcript import transcript_to_docx, transcript_to_pdf
from app.ui.i18n import Translator


def _watermark_color(name: str) -> tuple[float, float, float]:
    return {
        "Black": (0, 0, 0),
        "Gray": (0.45, 0.45, 0.45),
        "Blue": (0.05, 0.2, 0.8),
        "Red": (0.8, 0, 0),
    }.get(name, (0.8, 0, 0))


class DropList(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        self.status_callback = None
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setMinimumHeight(110)
        self.setAlternatingRowColors(True)

    def dragEnterEvent(self, event):  # noqa: N802 - Qt API
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):  # noqa: N802 - Qt API
        event.acceptProposedAction()

    def dropEvent(self, event):  # noqa: N802 - Qt API
        for url in event.mimeData().urls():
            if url.isLocalFile():
                self.add_file(url.toLocalFile())

    def add_file(self, path: str, notify: bool = True) -> None:
        item = QListWidgetItem(path)
        item.setToolTip(path)
        self.addItem(item)
        if notify and self.status_callback:
            self.status_callback(f"Added file: {path}")

    def paths(self) -> list[str]:
        return [self.item(i).text() for i in range(self.count())]

    def move_selected(self, direction: int) -> None:
        row = self.currentRow()
        target = row + direction
        if row < 0 or target < 0 or target >= self.count():
            return
        item = self.takeItem(row)
        self.insertItem(target, item)
        self.setCurrentRow(target)


class ModulePage(QWidget):
    def __init__(self, title: str, log_callback) -> None:
        super().__init__()
        self.log_callback = log_callback
        self.files = DropList()
        self.files.status_callback = self.add_status
        self.output = QLineEdit(str(Path.cwd() / "output"))
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.status_log = QPlainTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.setMaximumHeight(120)
        self.options = QFormLayout()
        self.run_button = QPushButton("Run")
        self.add_files_button = QPushButton("Add Files")
        self.clear_button = QPushButton("Clear")
        self.up_button = QPushButton("Move Up")
        self.down_button = QPushButton("Move Down")

        root = QVBoxLayout(self)
        heading = QLabel(title)
        heading.setObjectName("ModuleTitle")
        root.addWidget(heading)
        root.addWidget(QLabel("Drop files here or add them manually. Processing is local by default."))
        root.addWidget(self.files)

        file_buttons = QHBoxLayout()
        file_buttons.addWidget(self.add_files_button)
        file_buttons.addWidget(self.up_button)
        file_buttons.addWidget(self.down_button)
        file_buttons.addWidget(self.clear_button)
        file_buttons.addStretch(1)
        root.addLayout(file_buttons)

        options_box = QFrame()
        options_box.setObjectName("OptionsBox")
        options_box.setLayout(self.options)
        root.addWidget(options_box)

        out_row = QHBoxLayout()
        out_row.addWidget(QLabel("Output path/folder"))
        out_row.addWidget(self.output)
        browse = QPushButton("Browse")
        out_row.addWidget(browse)
        root.addLayout(out_row)
        root.addWidget(self.progress)
        root.addWidget(self.run_button)
        root.addWidget(QLabel("Status Log"))
        root.addWidget(self.status_log)
        root.addStretch(1)

        self.add_files_button.clicked.connect(self.add_files)
        self.up_button.clicked.connect(lambda: self._move_file(-1))
        self.down_button.clicked.connect(lambda: self._move_file(1))
        self.clear_button.clicked.connect(self.clear_files)
        browse.clicked.connect(self.browse_output)

    def add_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(self, "Select files")
        for path in paths:
            self.files.add_file(path, notify=False)
        if paths:
            self.add_status(f"Added {len(paths)} file(s).")

    def browse_output(self) -> None:
        current = self.output.text().strip()
        if Path(current).suffix:
            path, _ = QFileDialog.getSaveFileName(self, "Select output", current)
        else:
            path = QFileDialog.getExistingDirectory(self, "Select output folder", current)
        if path:
            self.output.setText(path)
            self.add_status(f"Output set to: {path}")

    def run_safely(self, action) -> None:
        try:
            self.add_status("Processing started.")
            self.progress.setValue(10)
            result = action()
            self.progress.setValue(100)
            self.add_status(f"Done: {result}")
        except Exception as exc:
            self.progress.setValue(0)
            self.add_status(f"Error: {exc}")
            QMessageBox.critical(self, "Wallace's PDFirst", str(exc))

    def add_status(self, message: str) -> None:
        self.status_log.appendPlainText(message)
        self.log_callback(message)

    def clear_files(self) -> None:
        self.files.clear()
        self.add_status("File list cleared.")

    def _move_file(self, direction: int) -> None:
        before = self.files.currentRow()
        self.files.move_selected(direction)
        after = self.files.currentRow()
        if before != after and after >= 0:
            self.add_status("File order updated.")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.trn = Translator("en")
        self.setWindowTitle(self.trn.t("app_title"))
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.stack = QStackedWidget()
        self.nav = QListWidget()
        self.nav.setFixedWidth(230)

        central = QWidget()
        root = QHBoxLayout(central)
        root.addWidget(self.nav)
        content = QVBoxLayout()
        content.addWidget(self.stack, 1)
        content.addWidget(QLabel(self.trn.t("log")))
        content.addWidget(self.log, 0)
        root.addLayout(content, 1)
        self.setCentralWidget(central)

        self._build_pages()
        self._apply_style()
        self.log.clear()
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)

    def add_log(self, message: str) -> None:
        self.log.appendPlainText(message)

    def _add_page(self, key: str, page: QWidget) -> None:
        self.nav.addItem(self.trn.t(key))
        self.stack.addWidget(page)

    def _build_pages(self) -> None:
        self._add_page("split", self._split_page())
        self._add_page("merge", self._merge_page())
        self._add_page("image_pdf", self._image_page())
        self._add_page("rotate", self._rotate_page())
        self._add_page("transcript", self._transcript_page())
        self._add_page("watermark", self._watermark_page())
        self._add_page("settings", self._settings_page())
        self._add_page("about", self._about_page())

    def _image_page(self) -> ModulePage:
        page = ModulePage("Image to PDF", self.add_log)
        mode = QComboBox()
        mode.addItems(["fit_a4", "preserve"])
        orientation = QComboBox()
        orientation.addItems(["portrait", "landscape"])
        margin = QSpinBox()
        margin.setRange(0, 144)
        margin.setValue(36)
        page.options.addRow("Sizing", mode)
        page.options.addRow("Orientation", orientation)
        page.options.addRow("Margin (pt)", margin)
        page.output.setText(str(Path.cwd() / "output" / "images.pdf"))
        page.run_button.clicked.connect(
            lambda: page.run_safely(
                lambda: image_files_to_pdf(
                    page.files.paths(),
                    page.output.text(),
                    mode.currentText(),
                    orientation.currentText(),
                    margin.value(),
                )
            )
        )
        return page

    def _transcript_page(self) -> ModulePage:
        page = ModulePage("Transcript to Word/PDF", self.add_log)
        fmt = QComboBox()
        fmt.addItems(["docx", "pdf"])
        keep_time = QCheckBox("Keep timestamps")
        keep_speaker = QCheckBox("Keep speaker labels")
        keep_speaker.setChecked(True)
        dedupe = QCheckBox("Clean duplicated lines")
        dedupe.setChecked(True)
        grouping = QCheckBox("Paragraph grouping")
        grouping.setChecked(True)
        page.options.addRow("Output format", fmt)
        page.options.addRow("", keep_time)
        page.options.addRow("", keep_speaker)
        page.options.addRow("", dedupe)
        page.options.addRow("", grouping)
        page.output.setText(str(Path.cwd() / "output" / "transcript.docx"))

        def run():
            source = page.files.paths()[0]
            if fmt.currentText() == "docx":
                return transcript_to_docx(
                    source,
                    page.output.text(),
                    keep_time.isChecked(),
                    keep_speaker.isChecked(),
                    dedupe.isChecked(),
                    grouping.isChecked(),
                )
            return transcript_to_pdf(
                source,
                page.output.text(),
                keep_time.isChecked(),
                keep_speaker.isChecked(),
                dedupe.isChecked(),
                grouping.isChecked(),
            )

        page.run_button.clicked.connect(lambda: page.run_safely(run))
        return page

    def _merge_page(self) -> ModulePage:
        page = ModulePage("Merge PDF", self.add_log)
        page.output.setText(str(Path.cwd() / "output" / "merged.pdf"))
        page.run_button.clicked.connect(lambda: page.run_safely(lambda: merge_pdfs(page.files.paths(), page.output.text())))
        return page

    def _split_page(self) -> ModulePage:
        page = ModulePage("Split PDF", self.add_log)
        mode = QComboBox()
        mode.addItems(["custom_ranges", "burst_single_pages", "even_pages", "odd_pages"])
        ranges = QLineEdit("1-1, 2-3, 4-end")
        page.options.addRow("Split option", mode)
        page.options.addRow("Ranges", ranges)
        page.output.setText(str(Path.cwd() / "output" / "split"))
        page.run_button.clicked.connect(
            lambda: page.run_safely(lambda: split_pdf_by_mode(page.files.paths()[0], page.output.text(), mode.currentText(), ranges.text()))
        )
        return page

    def _rotate_page(self) -> ModulePage:
        page = ModulePage("Rotate PDF", self.add_log)
        angle = QComboBox()
        angle.addItems(["90", "180", "270"])
        ranges = QLineEdit("1-end")
        page.options.addRow("Clockwise Angle", angle)
        page.options.addRow("Pages", ranges)
        page.output.setText(str(Path.cwd() / "output" / "rotated.pdf"))
        page.run_button.clicked.connect(
            lambda: page.run_safely(lambda: rotate_pdf(page.files.paths()[0], page.output.text(), int(angle.currentText()), ranges.text()))
        )
        return page

    def _watermark_page(self) -> ModulePage:
        page = ModulePage("Add Watermark", self.add_log)
        kind = QComboBox()
        kind.addItems(["text", "image"])
        text = QLineEdit("CONFIDENTIAL")
        font = QComboBox()
        font.addItems(["Helvetica", "Times", "Courier"])
        font_size = QSpinBox()
        font_size.setRange(8, 160)
        font_size.setValue(48)
        bold = QCheckBox("Bold")
        italic = QCheckBox("Italic")
        underline = QCheckBox("Underline")
        color = QComboBox()
        color.addItems(["Red", "Black", "Gray", "Blue"])
        position = QComboBox()
        position.addItems(["center", "top-left", "top-right", "bottom-left", "bottom-right", "tiled"])
        transparency = QSpinBox()
        transparency.setRange(0, 95)
        transparency.setValue(75)
        transparency.setSuffix("% transparent")
        rotation = QSpinBox()
        rotation.setRange(0, 359)
        rotation.setValue(35)
        rotation.setSuffix(" degrees clockwise")
        image = QLineEdit("")
        image_browse = QPushButton("Browse")
        image_row = QHBoxLayout()
        image_row.addWidget(image)
        image_row.addWidget(image_browse)
        image_widget = QWidget()
        image_widget.setLayout(image_row)
        ranges = QLineEdit("1-end")
        page.options.addRow("Type", kind)
        page.options.addRow("Text", text)
        page.options.addRow("Font", font)
        page.options.addRow("Font size", font_size)
        page.options.addRow("", bold)
        page.options.addRow("", italic)
        page.options.addRow("", underline)
        page.options.addRow("Text color", color)
        page.options.addRow("Position", position)
        page.options.addRow("Transparency", transparency)
        page.options.addRow("Clockwise rotation", rotation)
        page.options.addRow("Image path", image_widget)
        page.options.addRow("Pages", ranges)
        page.output.setText(str(Path.cwd() / "output" / "watermarked.pdf"))
        image_browse.clicked.connect(lambda: self._choose_file(image, "Images (*.png *.jpg *.jpeg);;All files (*.*)"))

        def run():
            opacity = max(0.0, min(1.0, (100 - transparency.value()) / 100))
            if kind.currentText() == "image":
                return add_image_watermark(
                    page.files.paths()[0],
                    page.output.text(),
                    image.text(),
                    opacity=opacity,
                    position=position.currentText(),
                    page_ranges=ranges.text(),
                )
            return add_text_watermark(
                page.files.paths()[0],
                page.output.text(),
                text.text(),
                font_size=font_size.value(),
                opacity=opacity,
                rotation=rotation.value(),
                position=position.currentText(),
                page_ranges=ranges.text(),
                font_name=font.currentText(),
                bold=bold.isChecked(),
                italic=italic.isChecked(),
                underline=underline.isChecked(),
                color=_watermark_color(color.currentText()),
            )

        page.run_button.clicked.connect(lambda: page.run_safely(run))
        return page

    def _settings_page(self) -> ModulePage:
        page = ModulePage("Settings", self.add_log)
        language = QComboBox()
        language.addItems(["English", "Traditional Chinese", "Simplified Chinese"])
        privacy = QCheckBox("Privacy mode: process files locally unless optional API mode is explicitly enabled")
        privacy.setChecked(True)
        api = QLineEdit()
        api.setEchoMode(QLineEdit.Password)
        page.options.addRow("Language", language)
        page.options.addRow("", privacy)
        page.options.addRow("Optional OpenAI API key", api)
        page.run_button.setText("Save Settings")
        page.run_button.clicked.connect(lambda: self.add_log("Settings kept for this session."))
        return page

    def _about_page(self) -> QWidget:
        page = QWidget()
        root = QVBoxLayout(page)
        heading = QLabel("About Wallace's PDFirst")
        heading.setObjectName("ModuleTitle")
        root.addWidget(heading)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        body = QWidget()
        body_layout = QVBoxLayout(body)
        content = QLabel(
            "About Wallace's PDFirst\n\n"
            "Wallace's PDFirst is a portable Windows desktop application designed for practical document workflows, "
            "including PDF splitting, merging, rotation, image-to-PDF conversion, transcript conversion, and watermarking.\n\n"
            "The application was conceived by Wallace, a non-programmer, an AI enthusiast, and a Hong Kong listed-company "
            "governance and compliance professional.\n\n"
            "This app is built around a simple principle: important document work should be fast, traceable, "
            "privacy-conscious, and easy to perform without complicated installation.\n\n"
            "Key principles:\n\n"
            "* Portable: open directly from the .exe file.\n"
            "* Practical: built for real PDF, worksheet, and transcript workflows.\n"
            "* Local-first: core functions are processed on the user's computer.\n"
            "* Reviewable: advanced functions should allow user preview and manual checking.\n"
            "* Responsible: users should only process files they own or are authorized to modify.\n\n"
            "Support this project:\n"
            "If you find Wallace's PDFirst useful, please support the project by starring the GitHub repository. "
            "Your star helps encourage further development, improvements, and new practical features.\n\n"
            "Disclaimer:\n"
            "Wallace's PDFirst is provided as a practical document-processing tool. It is not legal, professional, "
            "academic, or examination advice. Users are responsible for checking the accuracy, completeness, legality, "
            "and suitability of all output files before use, submission, publication, or distribution.\n\n"
            "Document-editing features must only be used on files that the user owns, has created, or is legally authorized "
            "to modify. The application must not be used to remove copyright notices, ownership marks, third-party attribution, "
            "anti-piracy marks, or other protected identifiers without proper authorization.\n\n"
            "Copyright:\n"
            "Copyright (c) 2026 Wallace. All rights reserved unless otherwise stated in the applicable repository license.\n\n"
            "No patent, registered trademark, or exclusive statutory intellectual property right is claimed unless expressly stated. "
            "Product names, third-party libraries, file formats, and trademarks belong to their respective owners.\n\n"
            "Version: 1.0 Portable\n"
            "Developer / Concept: Wallace\n"
            "GitHub: Please star the repository if you like this project."
        )
        content.setWordWrap(True)
        content.setTextInteractionFlags(Qt.TextSelectableByMouse)
        content.setObjectName("AboutText")
        body_layout.addWidget(content)
        body_layout.addStretch(1)
        scroll.setWidget(body)
        root.addWidget(scroll, 1)
        return page

    def _file_row(self, target: QLineEdit, file_filter: str) -> QWidget:
        browse = QPushButton("Browse")
        browse.clicked.connect(lambda: self._choose_file(target, file_filter))
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.addWidget(target)
        row.addWidget(browse)
        widget = QWidget()
        widget.setLayout(row)
        return widget

    def _choose_file(self, target: QLineEdit, file_filter: str) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select file", target.text(), file_filter)
        if path:
            target.setText(path)

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            * { font-family: "Segoe UI", "Microsoft JhengHei UI", "Microsoft YaHei UI", "Arial", sans-serif; }
            QWidget { background: #f6f7f9; color: #111827; }
            QMainWindow { background: #f6f7f9; color: #111827; }
            QLabel { color: #111827; background: transparent; }
            QListWidget {
                border: none;
                background: #ffffff;
                color: #111827;
                font-size: 14px;
                outline: 0;
            }
            QListWidget::item {
                color: #111827;
                padding: 12px;
                border-bottom: 1px solid #eceff3;
                background: #ffffff;
            }
            QListWidget::item:hover { background: #f3f6fb; color: #111827; }
            QListWidget::item:selected { background: #e8f0fe; color: #174ea6; }
            QLabel#ModuleTitle { font-size: 28px; font-weight: 700; color: #202124; margin: 8px 0; }
            QLabel#AboutText { font-size: 14px; line-height: 1.35; color: #202124; padding: 12px; }
            QFrame#OptionsBox { background: #ffffff; color: #111827; border: 1px solid #dde2ea; border-radius: 8px; padding: 10px; }
            QPushButton { padding: 8px 14px; border-radius: 6px; background: #2563eb; color: white; border: none; }
            QPushButton:hover { background: #1d4ed8; }
            QPushButton:disabled { background: #94a3b8; color: #f8fafc; }
            QCheckBox { color: #111827; background: transparent; spacing: 6px; }
            QCheckBox::indicator { background: #ffffff; border: 1px solid #64748b; width: 14px; height: 14px; }
            QCheckBox::indicator:checked { background: #2563eb; border: 1px solid #2563eb; }
            QLineEdit, QComboBox, QSpinBox, QPlainTextEdit {
                color: #111827;
                padding: 6px;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                background: white;
                selection-background-color: #bfdbfe;
                selection-color: #111827;
            }
            QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled, QPlainTextEdit:disabled {
                color: #64748b;
                background: #f1f5f9;
            }
            QComboBox QAbstractItemView {
                background: #ffffff;
                color: #111827;
                selection-background-color: #e8f0fe;
                selection-color: #174ea6;
                border: 1px solid #cbd5e1;
            }
            QProgressBar {
                color: #111827;
                background: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk { background: #2563eb; border-radius: 4px; }
            QScrollArea { border: 1px solid #dde2ea; border-radius: 8px; background: #ffffff; color: #111827; }
            QScrollArea QWidget { background: #ffffff; color: #111827; }
            """
        )
