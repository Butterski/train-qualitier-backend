from flask import Flask
import sqlite3

app = Flask(__name__)

app.config.from_pyfile("config.py")


def get_db_conn():
    conn = sqlite3.connect(app.config["DATABASE"])
    return conn


from app import routes
