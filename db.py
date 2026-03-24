import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="vijay",
        password="1234",
        database="network_db"
    )

def insert_log(ip, status):
    conn = connect_db()
    cursor = conn.cursor()

    query = "INSERT INTO network_logs (ip_address, status) VALUES (%s, %s)"
    values = (ip, status)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
