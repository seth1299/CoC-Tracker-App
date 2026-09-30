"""Main Qt window for the CoC Tracker application."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from coc_tracker.database import Database


class MainWindow(QMainWindow):
    """Display a minimal database-backed CoC Tracker interface."""

    def __init__(self, database: Database) -> None:
        super().__init__()
        self.database = database

        self.setWindowTitle("CoC Tracker")
        self.resize(760, 480)
        self.setMinimumSize(560, 360)

        title = QLabel("Coordination-of-Care Tracker")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        database_label = QLabel(f"Database: {database.path}")
        database_label.setWordWrap(True)
        database_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Enter a temporary note to test storage…")
        self.note_input.returnPressed.connect(self.save_note)

        save_button = QPushButton("Save note")
        save_button.clicked.connect(self.save_note)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.note_input, stretch=1)
        input_layout.addWidget(save_button)

        self.notes_list = QListWidget()
        self.notes_list.setAlternatingRowColors(True)

        refresh_button = QPushButton("Refresh from database")
        refresh_button.clicked.connect(self.load_notes)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(database_label)
        layout.addSpacing(12)
        layout.addLayout(input_layout)
        layout.addWidget(self.notes_list, stretch=1)
        layout.addWidget(refresh_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.statusBar().showMessage("Ready")

        self.setStyleSheet(
            """
            QLabel#title {
                font-size: 22px;
                font-weight: 600;
                padding: 12px;
            }
            QLineEdit, QListWidget {
                font-size: 14px;
            }
            QLineEdit {
                padding: 7px;
            }
            QPushButton {
                padding: 7px 12px;
            }
            """
        )
        self.load_notes()

    def save_note(self) -> None:
        """Persist the current note and refresh the visible list."""
        try:
            note_id = self.database.add_note(self.note_input.text())
        except ValueError as error:
            QMessageBox.information(self, "Nothing to save", str(error))
            return
        except Exception as error:
            QMessageBox.critical(self, "Database error", str(error))
            return

        self.note_input.clear()
        self.load_notes()
        self.statusBar().showMessage(f"Saved note {note_id}", 5000)

    def load_notes(self) -> None:
        """Reload all notes from SQLite into the list widget."""
        try:
            notes = self.database.list_notes()
        except Exception as error:
            QMessageBox.critical(self, "Database error", str(error))
            return

        self.notes_list.clear()
        for note in notes:
            item = QListWidgetItem(
                f"{note['created_at']}  —  {note['body']}"
            )
            item.setData(Qt.ItemDataRole.UserRole, note["note_id"])
            self.notes_list.addItem(item)

        count = len(notes)
        self.statusBar().showMessage(
            f"Loaded {count} note{'s' if count != 1 else ''}", 5000
        )
