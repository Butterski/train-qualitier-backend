import sqlite3
import os


def initialize_database(measurement_name, measurement_grade):
    db_dir = "./database"
    db_file = os.path.join(db_dir, "database.sqlite")
    os.makedirs(db_dir, exist_ok=True)  # Create directory if it does not exist
    if not os.path.exists(db_file):
        open(db_file, "w").close()

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS measurements_data (
            id INTEGER PRIMARY KEY,
            measurement_name TEXT,
            measurement_grade TEXT
        )
    """
    )

    cursor.execute(
        """
        INSERT INTO measurements_data (measurement_name, measurement_grade)
        VALUES (?, ?)
    """,
        (measurement_name, measurement_grade),
    )
    measurement_id = cursor.lastrowid

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS measurement_{measurement_id} (
            timestamp TIMESTAMP,
            x_axis REAL,
            y_axis REAL,
            z_axis REAL,
            temperature REAL,
            magnetometer REAL
        )
    """
    )

    conn.commit()
    conn.close()

    return measurement_id
