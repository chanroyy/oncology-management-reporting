
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

departments = [
    "Medical Oncology",
    "Radiation Oncology",
    "Hematology",
    "Surgical Oncology"
]

statuses = [
    "Completed",
    "Cancelled",
    "No-show"
]

output = Path("oncology_appointments.csv")

start_date = date(2026, 1, 1)

with output.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "appointment_id",
        "patient_id",
        "appointment_date",
        "department",
        "status"
    ])

    for appointment_id in range(1, 501):
        patient_id = random.randint(1001, 1150)
        appointment_date = start_date + timedelta(
            days=random.randint(0, 304)
        )

        department = random.choice(departments)

        status = random.choices(
            statuses,
            weights=[80, 12, 8],
            k=1
        )[0]

        writer.writerow([
            appointment_id,
            patient_id,
            appointment_date.isoformat(),
            department,
            status
        ])

print("Synthetic oncology dataset created successfully!")
print("Total appointments: 500")
print(f"Saved to: {output.resolve()}")
