
import csv
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import etl_pipeline


class TestOncologyETL(unittest.TestCase):

    def test_generated_data_is_valid(self):
        records = etl_pipeline.extract_and_validate()
        self.assertEqual(len(records), 500)
        self.assertEqual(
            len({row[0] for row in records}), 500
        )

    def test_invalid_status_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            csv_path = Path(folder) / "invalid.csv"

            with csv_path.open(
                "w", newline="", encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow([
                    "appointment_id",
                    "patient_id",
                    "appointment_date",
                    "department",
                    "status"
                ])
                writer.writerow([
                    1, 1001, "2026-01-01",
                    "Medical Oncology", "Unknown"
                ])

            with patch.object(
                etl_pipeline, "CSV_FILE", csv_path
            ):
                with self.assertRaises(ValueError):
                    etl_pipeline.extract_and_validate()

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            csv_path = Path(folder) / "duplicates.csv"

            with csv_path.open(
                "w", newline="", encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow([
                    "appointment_id",
                    "patient_id",
                    "appointment_date",
                    "department",
                    "status"
                ])

                for _ in range(2):
                    writer.writerow([
                        1, 1001, "2026-01-01",
                        "Hematology", "Completed"
                    ])

            with patch.object(
                etl_pipeline, "CSV_FILE", csv_path
            ):
                with self.assertRaises(ValueError):
                    etl_pipeline.extract_and_validate()

    def test_loading_is_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            db_path = Path(folder) / "test.db"

            records = [
                (1, 1001, "2026-01-01",
                 "Medical Oncology", "Completed")
            ]

            with patch.object(
                etl_pipeline, "DB_FILE", db_path
            ):
                etl_pipeline.load_database(records)
                count = etl_pipeline.load_database(records)

            self.assertEqual(count, 1)

            with closing(sqlite3.connect(db_path)) as conn:
                actual = conn.execute(
                    "SELECT COUNT(*) FROM appointments"
                ).fetchone()[0]

            self.assertEqual(actual, 1)


if __name__ == "__main__":
    unittest.main()
