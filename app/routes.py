from app import app, get_db_conn

@app.route('/testdb')
def testdb():
    db = get_db_conn()
    cur = db.cursor()
    cur.execute('SELECT * FROM my_table')
    results = cur.fetchall()
    return str(results)