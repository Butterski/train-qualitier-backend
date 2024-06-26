import sqlite3


def initialize_database(measurement_name, measurement_grade):
    db_file = "./database/database.sqlite"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS measurements_data (
            id INTEGER PRIMARY KEY,
            measurement_name TEXT,
            measurement_grade TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            gyro_x REAL,
            gyro_y REAL,
            gyro_z REAL,
            acceleratior_x REAL,
            acceleratior_y REAL,
            acceleration_z REAL,
            magnetometer_x REAL,
            magnetometer_y REAL,
            magnetometer_z REAL,
            temperature REAL,
            humidity REAL
        )
    """
    )

    conn.commit()
    conn.close()

    return measurement_id
