from flask import Flask, render_template, request
import datetime
import psycopg2

"""
dum = [
  ['arne', '013-131313'], ['berith','01234'], ['caesar','077-1212321']
]
"""

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host = "localhost",
        database = "web_phonedb",
        user = "postgres",
        password = "continuousimpliesintegrable"
        )

conn = get_db_connection()

@app.route("/")
def start():
    now = datetime.datetime.now()
    D = [str(now.year%100), str(now.month), str(now.day)]
    if len(D[1])<2:
        D[1] = '0'+D[1]
    if len(D[2])<2:
        D[2] = '0'+D[2]
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonelist")
    rows = cur.fetchall()
    rows = [item[1:] for item in rows]
    cur.close()

    return render_template('list.html', list=rows, date=D)

@app.route("/delete")
def delete():
    name = request.args['name']
    cur = conn.cursor()
    cur.execute(f"DELETE FROM phonelist WHERE name='{name}';")
    cur.close()
    conn.commit()
    return render_template('delete.html', name=name)

@app.route("/insert")
def insert():
    name = request.args['name']
    phone = request.args['phone']
    address = request.args['address']
    email = request.args['email']
    cur = conn.cursor()
    cur.execute(f"INSERT INTO phonelist (name, phone, address, email) VALUES ('{name}','{phone}','{address}','{email}')")
    cur.close()
    conn.commit()
    return render_template("insert.html", **request.args)


# kör med
# flask --app app --debug run 