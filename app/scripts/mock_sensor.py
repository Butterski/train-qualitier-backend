import sqlite3
import threading
import time
import random


class SensorThread(threading.Thread):
    def __init__(self, measurement_id):
        super().__init__()
        self.measurement_id = measurement_id
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def pause(self):
        self._pause_event.set()

    def resume(self):
        self._pause_event.clear()

    def run(self):
        start_time = time.time()
        while not self._stop_event.is_set() and not self._pause_event.is_set():
            if time.time() - start_time > 3600:
                self.stop()
            if not self._pause_event.is_set():
                mock_sensor(self.measurement_id)
            time.sleep(0.5)


def mock_sensor(measurement_id):
    # timestamp = "CURRENT_TIMESTAMP"
    timestamp = time.time()
    x_axis = round(random.uniform(0.0, 2.0), 4)
    y_axis = round(random.uniform(0.0, 2.0), 4)
    z_axis = round(random.uniform(0.0, 2.0), 4)
    temperature =round(random.uniform(10.0, 30.0), 2)
    magnetometer = round(random.uniform(0.0, 100.0), 4)

    conn = sqlite3.connect("database/database.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO measurement_{measurement_id} VALUES ({timestamp}, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (x_axis, y_axis, z_axis, temperature, magnetometer, x_axis, y_axis, z_axis, z_axis,  y_axis, z_axis),
    )
    conn.commit()
    conn.close()
