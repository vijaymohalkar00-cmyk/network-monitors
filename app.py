from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="vijay",
        password="1234",
        database="network_db"
    )

    cursor = conn.cursor()

    # Show latest 20 records
    cursor.execute("SELECT * FROM network_logs ORDER BY id DESC LIMIT 20")
    data = cursor.fetchall()

    conn.close()
    return data

@app.route("/")
def home():
    data = get_data()
    return render_template("index.html", data=data)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
