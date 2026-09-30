from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from coc_tracker.database import Database


class DatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.database = Database(
            Path(self.temporary_directory.name) / "nested" / "tracker.db"
        )
        self.database.initialize()

    def test_initialize_creates_database_and_empty_notes_table(self) -> None:
        self.assertTrue(self.database.path.is_file())
        self.assertEqual(self.database.list_notes(), [])

    def test_add_and_list_notes(self) -> None:
        first_id = self.database.add_note(" First note ")
        second_id = self.database.add_note("Second note")

        notes = self.database.list_notes()

        self.assertEqual([row["note_id"] for row in notes], [second_id, first_id])
        self.assertEqual([row["body"] for row in notes], ["Second note", "First note"])

    def test_add_note_rejects_blank_text(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.database.add_note("   ")


if __name__ == "__main__":
    unittest.main()
