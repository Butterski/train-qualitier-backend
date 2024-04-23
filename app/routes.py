from app import app, get_db_conn
from app.db_init import initialize_database
from .scripts.mock_sensor import SensorThread

sensor_threads = {}


@app.route("/testdb")
def testdb():
    db = get_db_conn()
    cur = db.cursor()
    cur.execute("SELECT * FROM measurements_data")
    results = cur.fetchall()
    return results


@app.route("/measurement/create/<measurement_name>")
def create_measurement(measurement_name):
    measurement_id = initialize_database(measurement_name, "")

    return {"measurement_id": measurement_id, "measurement_name": measurement_name}


@app.route("/measurement/start/<int:measurement_id>")
def start_measurement(measurement_id):
    if (
        measurement_id not in sensor_threads
        or not sensor_threads[measurement_id].is_alive()
    ):
        sensor_threads[measurement_id] = SensorThread(measurement_id)
        sensor_threads[measurement_id].start()
        return {
            "status": "success",
            "message": f"Measurement {measurement_id} started.",
        }
    else:
        return {
            "status": "error",
            "message": f"Measurement {measurement_id} is already running.",
        }


@app.route("/measurement/stop/<int:measurement_id>")
def stop_measurement(measurement_id):
    if measurement_id in sensor_threads and sensor_threads[measurement_id].is_alive():
        sensor_threads[measurement_id].stop()
        sensor_threads[measurement_id].join()
        del sensor_threads[measurement_id]
        return {
            "status": "success",
            "message": f"Measurement {measurement_id} stopped.",
        }
    else:
        return {
            "status": "error",
            "message": f"No active measurement found for ID {measurement_id}.",
        }


@app.route("/measurement/pause/<int:measurement_id>")
def pause_measurement(measurement_id):
    if measurement_id in sensor_threads and sensor_threads[measurement_id].is_alive():
        sensor_threads[measurement_id].pause()
        return {"status": "success", "message": f"Measurement {measurement_id} paused."}
    else:
        return {
            "status": "error",
            "message": f"No active measurement found for ID {measurement_id}.",
        }


@app.route("/measurement/<int:measurement_id>")
def resume_measurement(measurement_id):
    if measurement_id in sensor_threads and sensor_threads[measurement_id].is_alive():
        sensor_threads[measurement_id].resume()
        return {
            "status": "success",
            "message": f"Measurement {measurement_id} resumed.",
        }
    else:
        return {
            "status": "error",
            "message": f"No active measurement found for ID {measurement_id}.",
        }


@app.route("/get_measurement_log/<measurement_id>")
def get_measurement_log(measurement_id):
    db = get_db_conn()
    cur = db.cursor()
    cur.execute(
        f"SELECT * FROM measurement_{measurement_id} ORDER BY timestamp DESC LIMIT 1"
    )
    results = cur.fetchall()
    return results


@app.route("/get_measurement_data/<measurement_id>")
def get_measurement_data(measurement_id):
    db = get_db_conn()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM measurement_{measurement_id}")
    results = cur.fetchall()
    return results
