import os
import socket
import time
import smtplib
from email.mime.text import MIMEText
from db import insert_log

# -------------------------
# CONFIG
# -------------------------
ips = ["8.8.8.8", "1.1.1.1", "google.com"]

EMAIL_SENDER = "vijaymohalkar00@gmail.com"
EMAIL_PASSWORD = "abcd efgh ijkl mnop"  # app password
EMAIL_RECEIVER = "vijaymohalkar2000@gmail.com"

alerted = set()  # to avoid duplicate alerts

# -------------------------
# HOST CHECK
# -------------------------
def check_host(ip):
    try:
        response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")
        return "UP" if response == 0 else "DOWN"
    except:
        return "ERROR"

# -------------------------
# PORT CHECK
# -------------------------
def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        result = sock.connect_ex((ip, port))
        sock.close()

        return "OPEN" if result == 0 else "CLOSED"
    except:
        return "ERROR"

# -------------------------
# EMAIL ALERT
# -------------------------
def send_email_alert(ip):
    subject = f"ALERT: {ip} is DOWN"
    body = f"Server {ip} is not reachable."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print(f"📧 Email alert sent for {ip}")

    except Exception as e:
        print(f"Email error: {e}")

# -------------------------
# MAIN LOOP
# -------------------------
while True:
    for ip in ips:
        try:
            status = check_host(ip)
            port_status = check_port(ip, 80)

            print(f"{ip} is {status}, Port 80 is {port_status}")

            # Save to DB
            insert_log(ip, status)

            # Send alert only once
            if status == "DOWN" and ip not in alerted:
                send_email_alert(ip)
                alerted.add(ip)

            # Reset alert if back UP
            if status == "UP" and ip in alerted:
                alerted.remove(ip)

        except Exception as e:
            print(f"Error checking {ip}: {e}")

    time.sleep(10)  # interval
