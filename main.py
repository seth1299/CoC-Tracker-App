"""Application entry point for CoC Tracker."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox

from coc_tracker.database import Database
from coc_tracker.window import MainWindow


def application_directory() -> Path:
    """Return the source directory, or the executable directory when frozen."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def main() -> int:
    """Initialize the database and start the Qt event loop."""
    app = QApplication(sys.argv)
    app.setApplicationName("CoC Tracker")

    database = Database(application_directory() / "coc_tracker.db")
    try:
        database.initialize()
    except Exception as error:
        QMessageBox.critical(
            None,
            "Unable to open database",
            f"Could not initialize {database.path}:\n\n{error}",
        )
        return 1

    window = MainWindow(database)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
