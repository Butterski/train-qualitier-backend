from flask import Flask
import logging
from db_conn import get_db

app = Flask(__name__)

@app.route('/testdb')
def testdb():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM my_table')
    results = cur.fetchall()
    return str(results)

if __name__ == '__main__':
    app.run(port=2137, debug=True)