"""Application entry point for CoC Tracker."""

from __future__ import annotations

import sys
import logging
import os
import tempfile
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox

from coc_tracker.database import Database
from coc_tracker.window import MainWindow


LOGGER = logging.getLogger("coc_tracker")


class ApplicationLogFormatter(logging.Formatter):
    """Format application errors in the project's requested log format."""

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        timestamp = datetime.fromtimestamp(record.created)
        hour = timestamp.hour % 12 or 12
        suffix = "A.M." if timestamp.hour < 12 else "P.M."
        return f"{timestamp.month}.{timestamp.day}.{timestamp.strftime('%y')}, {hour}:{timestamp.minute:02d}:{timestamp.second:02d} {suffix}"

    def format(self, record: logging.LogRecord) -> str:
        record.log_severity = record.levelname.lower()
        return super().format(record)


def configure_logging(app_directory: Path) -> Path | None:
    """Configure a rotating error log, using a writable fallback if needed."""
    candidates = [app_directory]
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        candidates.append(Path(local_app_data) / "CoCTracker")
    candidates.append(Path(tempfile.gettempdir()) / "CoCTracker")

    handler: RotatingFileHandler | None = None
    log_path: Path | None = None
    for directory in candidates:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            log_path = directory / "app_errors.log"
            handler = RotatingFileHandler(
                log_path,
                maxBytes=1_000_000,
                backupCount=3,
                encoding="utf-8",
            )
            break
        except OSError:
            continue

    LOGGER.setLevel(logging.ERROR)
    LOGGER.propagate = False
    LOGGER.handlers.clear()
    if handler is None:
        LOGGER.addHandler(logging.NullHandler())
        return None

    handler.setFormatter(
        ApplicationLogFormatter(
            "%(asctime)s | %(log_severity)s | %(filename)s | %(funcName)s | %(message)s"
        )
    )
    LOGGER.addHandler(handler)
    return log_path


def handle_uncaught_exception(
    exception_type: type[BaseException],
    exception: BaseException,
    traceback: object,
) -> None:
    """Record an uncaught application exception and show a user-facing alert."""
    LOGGER.critical(
        "Uncaught application exception",
        exc_info=(exception_type, exception, traceback),
    )
    QMessageBox.critical(
        None,
        "Unexpected error",
        "The application encountered an unexpected error. Please contact support and provide the app_errors.log file.",
    )


def application_directory() -> Path:
    """Return the source directory, or the executable directory when frozen."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def main() -> int:
    """Initialize the database and start the Qt event loop."""
    log_path = configure_logging(application_directory())
    app = QApplication(sys.argv)
    app.setApplicationName("CoC Tracker")
    sys.excepthook = handle_uncaught_exception
    if log_path is None:
        LOGGER.error("Could not create app_errors.log in an available location")

    database = Database(application_directory() / "coc_tracker.db")
    try:
        database.initialize()
    except Exception as error:
        LOGGER.exception("Database initialization failed")
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
