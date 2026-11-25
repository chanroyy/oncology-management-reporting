
import sqlite3

DB_FILE = "oncology_reporting.db"

with sqlite3.connect(DB_FILE) as conn:
    total = conn.execute("""
        SELECT COUNT(*) FROM appointments
    """).fetchone()[0]

    print("\nONCOLOGY MANAGEMENT REPORT")
    print("=" * 40)
    print(f"Total appointments: {total}")

    print("\nAPPOINTMENT STATUS")
    print("-" * 40)

    results = conn.execute("""
        SELECT
            status,
            COUNT(*) AS appointment_count,
            ROUND(100.0 * COUNT(*) /
                (SELECT COUNT(*) FROM appointments), 1)
                AS percentage
        FROM appointments
        GROUP BY status
        ORDER BY appointment_count DESC
    """).fetchall()

    for status, count, percentage in results:
        print(f"{status}: {count} ({percentage}%)")

    print("\nDEPARTMENT ACTIVITY")
    print("-" * 40)

    results = conn.execute("""
        SELECT department, COUNT(*) AS total
        FROM appointments
        GROUP BY department
        ORDER BY total DESC
    """).fetchall()

    for department, count in results:
        print(f"{department}: {count}")

    print("\nMONTHLY APPOINTMENT VOLUMES")
    print("-" * 40)

    results = conn.execute("""
        SELECT
            strftime('%Y-%m', appointment_date) AS month,
            COUNT(*) AS total
        FROM appointments
        GROUP BY month
        ORDER BY month
    """).fetchall()

    for month, count in results:
        print(f"{month}: {count}")

print("\nManagement reporting completed successfully!")
