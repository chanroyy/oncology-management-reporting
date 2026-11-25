

import csv
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

CSV_FILE = Path("oncology_appointments.csv")
DB_FILE = Path("oncology_reporting.db")

VALID_STATUSES = {"Completed", "Cancelled", "No-show"}

VALID_DEPARTMENTS = {
    "Medical Oncology",
    "Radiation Oncology",
    "Hematology",
    "Surgical Oncology",
}


def extract_and_validate():
    records = []
    seen_ids = set()

    with CSV_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            appointment_id = int(row["appointment_id"])
            patient_id = int(row["patient_id"])
            appointment_date = date.fromisoformat(
                row["appointment_date"]
            )
            department = row["department"]
            status = row["status"]

            if appointment_id <= 0 or patient_id <= 0:
                raise ValueError("IDs must be positive")

            if appointment_id in seen_ids:
                raise ValueError("Duplicate appointment ID")

            if department not in VALID_DEPARTMENTS:
                raise ValueError("Invalid department")

            if status not in VALID_STATUSES:
                raise ValueError("Invalid appointment status")

            seen_ids.add(appointment_id)

            records.append((
                appointment_id,
                patient_id,
                appointment_date.isoformat(),
                department,
                status,
            ))

    if not records:
        raise ValueError("CSV contains no appointments")

    return records


def load_database(records):
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY,
                    patient_id INTEGER NOT NULL,
                    appointment_date TEXT NOT NULL,
                    department TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)

            conn.executemany("""
                INSERT INTO appointments (
                    appointment_id,
                    patient_id,
                    appointment_date,
                    department,
                    status
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(appointment_id) DO UPDATE SET
                    patient_id = excluded.patient_id,
                    appointment_date = excluded.appointment_date,
                    department = excluded.department,
                    status = excluded.status
            """, records)

            count = conn.execute(
                "SELECT COUNT(*) FROM appointments"
            ).fetchone()[0]

    return count


def main():
    print("Starting oncology ETL pipeline...")

    records = extract_and_validate()
    print(f"Validated records: {len(records)}")

    count = load_database(records)

    print(f"Database records: {count}")
    print("ETL pipeline completed successfully!")


if __name__ == "__main__":
    main()
