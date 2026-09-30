"""SQLite persistence for the CoC Tracker application."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    """Manage the application's local SQLite database."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def connect(self) -> sqlite3.Connection:
        """Open a configured connection to the database."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        """Create the initial schema when it does not already exist."""
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    body TEXT NOT NULL CHECK (length(trim(body)) > 0),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_note(self, body: str) -> int:
        """Store a note and return its generated identifier."""
        cleaned_body = body.strip()
        if not cleaned_body:
            raise ValueError("A note cannot be empty.")

        with self.connect() as connection:
            cursor = connection.execute(
                "INSERT INTO notes (body) VALUES (?)", (cleaned_body,)
            )
            if cursor.lastrowid is None:
                raise RuntimeError("SQLite did not return a note identifier.")
            return cursor.lastrowid

    def list_notes(self) -> list[sqlite3.Row]:
        """Return notes with the newest entries first."""
        with self.connect() as connection:
            return list(
                connection.execute(
                    """
                    SELECT note_id, body, created_at
                    FROM notes
                    ORDER BY note_id DESC
                    """
                )
            )
