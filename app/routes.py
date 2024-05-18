from app import app, get_db_conn
from app.db_init import initialize_database
from .scripts.get_sensor_data import SensorThread
from flask import jsonify
import json

sensor_threads = {}


@app.route("/api/testdb")
def testdb():
    db = get_db_conn()
    cur = db.cursor()
    cur.execute("SELECT * FROM measurements_data")
    results = cur.fetchall()
    return results


@app.route("/api/measurements")
def get_measurements():
    db = get_db_conn()
    cur = db.cursor()
    cur.execute("SELECT * FROM measurements_data")
    results = cur.fetchall()
    results = [
        {"id": r[0], "measurementName": r[1], "grade": r[2], "created_at": r[3]}
        for r in results
    ]
    return jsonify(results)


@app.route("/api/measurement/create/<measurement_name>")
def create_measurement(measurement_name):
    measurement_id = initialize_database(measurement_name, "")

    return jsonify(
        {"measurement_id": measurement_id, "measurement_name": measurement_name}
    )


@app.route("/api/measurement/start/<int:measurement_id>")
def start_measurement(measurement_id):
    if (
        measurement_id not in sensor_threads
        or not sensor_threads[measurement_id].is_alive()
    ):
        sensor_threads[measurement_id] = SensorThread(measurement_id)
        sensor_threads[measurement_id].start()
        return jsonify(
            {
                "status": "success",
                "message": f"Measurement {measurement_id} started.",
            }
        )
    else:
        return jsonify(
            {
                "status": "error",
                "message": f"Measurement {measurement_id} is already running.",
            }
        )


@app.route("/api/measurement/stop/<int:measurement_id>")
def stop_measurement(measurement_id):
    if measurement_id in sensor_threads and sensor_threads[measurement_id].is_alive():
        sensor_threads[measurement_id].stop()
        sensor_threads[measurement_id].join()
        del sensor_threads[measurement_id]
        return jsonify(
            {
                "status": "success",
                "message": f"Measurement {measurement_id} stopped.",
            }
        )
    else:
        return jsonify(
            {
                "status": "error",
                "message": f"No active measurement found for ID {measurement_id}.",
            }
        )


@app.route("/api/measurement/pause/<int:measurement_id>")
def pause_measurement(measurement_id):
    if measurement_id in sensor_threads and sensor_threads[measurement_id].is_alive():
        sensor_threads[measurement_id].pause()
        return jsonify(
            {"status": "success", "message": f"Measurement {measurement_id} paused."}
        )
    else:
        return jsonify(
            {
                "status": "error",
                "message": f"No active measurement found for ID {measurement_id}.",
            }
        )


@app.route("/api/measurement/<int:measurement_id>")
def resume_measurement(measurement_id):
    if measurement_id in sensor_threads and sensor_threads[measurement_id].is_alive():
        sensor_threads[measurement_id].resume()
        return jsonify(
            {
                "status": "success",
                "message": f"Measurement {measurement_id} resumed.",
            }
        )
    else:
        return jsonify(
            {
                "status": "error",
                "message": f"No active measurement found for ID {measurement_id}.",
            }
        )


@app.route("/api/get_measurement_log/<measurement_id>")
def get_measurement_log(measurement_id):
    db = get_db_conn()
    cur = db.cursor()
    cur.execute(
        f"SELECT * FROM measurement_{measurement_id} ORDER BY timestamp DESC LIMIT 1"
    )
    results = cur.fetchall()
    return jsonify(results)


@app.route("/api/get_measurement_data/<measurement_id>")
def get_measurement_data(measurement_id):
    db = get_db_conn()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM measurement_{measurement_id}")
    results = cur.fetchall()
    return jsonify(results)


@app.route("/api/get_mocked_measurement")
def get_mocked_measurement():
    with open("app/scripts/mock_data.json", "r") as f:
        results = json.load(f)
    return jsonify(results)


@app.route("/api/measurement/delete/<int:measurement_id>")
def delete_measurement(measurement_id):
    db = get_db_conn()
    cur = db.cursor()
    cur.execute(f"DROP TABLE measurement_{measurement_id}")
    cur.execute(f"DELETE FROM measurements_data WHERE id = {measurement_id}")
    db.commit()
    return jsonify(
        {"status": "success", "message": f"Measurement {measurement_id} deleted."}
    )


@app.route("/api/measurement/change_name/<int:measurement_id>/<new_name>")
def change_measurement_name(measurement_id, new_name):
    db = get_db_conn()
    cur = db.cursor()
    cur.execute(
        f"UPDATE measurements_data SET measurement_name = '{new_name}' WHERE id = {measurement_id}"
    )
    db.commit()
    return jsonify(
        {
            "status": "success",
            "message": f"Measurement {measurement_id} name changed to {new_name}.",
        }
    )


@app.route("/api/measurements/runnings")
def get_running_measurements_id():
    ids = [k for k, v in sensor_threads.items() if v.is_alive()]
    running_measurements = {}
    db = get_db_conn()
    cur = db.cursor()
    for id in ids:
        cur.execute(f"SELECT measurement_name FROM measurements_data WHERE id = {id}")
        name = cur.fetchone()[0]
        running_measurements[id] = name
    return jsonify(running_measurements)


@app.route("/api/measurements/is_running/<int:measurement_id>")
def is_measurement_running(measurement_id):
    db = get_db_conn()
    cur = db.cursor()
    cur.execute(
        f"SELECT measurement_name FROM measurements_data WHERE id = {measurement_id}"
    )
    measurement_name = cur.fetchone()[0]

    return jsonify(
        {
            "is_running": measurement_id in sensor_threads
            and sensor_threads[measurement_id].is_alive(),
            "measurement_id": measurement_id,
            "measurement_name": measurement_name,
        }
    )
