import board
import adafruit_ahtx0
import adafruit_icm20x
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
                add_sensor_data(self.measurement_id)
            time.sleep(0.5)


def add_sensor_data(measurement_id):
    timestamp = time.time()
    conn = sqlite3.connect("database/database.sqlite")
    cursor = conn.cursor()
    sensor_data = get_sensor_data()
    
    cursor.execute(
        f"INSERT INTO measurement_{measurement_id} VALUES ({timestamp},
        {sensor_data['acceleration']['x']}, {sensor_data['acceleration']['y']}, {sensor_data['acceleration']['z']},
        {sensor_data['gyro']['x']}, {sensor_data['gyro']['y']}, {sensor_data['gyro']['z']},
        {sensor_data['magnetometer']['x']}, {sensor_data['magnetometer']['y']}, {sensor_data['magnetometer']['z']},
        {sensor_data['temperature']}, {sensor_data['humidity']})
        "
    )
    conn.commit()
    conn.close()


def get_sensor_data():
    i2c = board.I2C()
    icm = adafruit_icm20x.ICM20948(i2c)
    sensor = adafruit_ahtx0.AHTx0(board.I2C())
    acceleration = icm.acceleration
    gyro = icm.gyro
    magnetometer = icm.magnetic
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    return {
        "acceleration": {
            "x": acceleration[0],
            "y": acceleration[1],
            "z": acceleration[2],
        },
        "gyro": {"x": gyro[0], "y": gyro[1], "z": gyro[2]},
        "magnetometer": {
            "x": magnetometer[0],
            "y": magnetometer[1],
            "z": magnetometer[2],
        },
        "temperature": temperature,
        "humidity": humidity,
    }
