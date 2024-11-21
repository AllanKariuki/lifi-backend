from flask import Flask, request
from flask_cors import CORS
from flask_sock import Sock
import json
from datetime import datetime
import threading
import time
import random

app = Flask(__name__)
CORS(app)
sock = Sock(app)

# Store connected clients
clients = set()


def generate_sensor_data():
    """Generate random sensor data within realistic ranges"""
    return {
        'humidity': round(random.uniform(30, 80), 1),  # 30-80%
        'temperature': round(random.uniform(15, 35), 1),  # 15-35°C
        'sunlight': round(random.uniform(0, 1000), 1),  # 0-1000 lux
        'water_content': round(random.uniform(20, 90), 1),  # 20-90%
        'growthRate': round(random.uniform(0, 5), 2),  # 0-5 cm/day
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }


def broadcast_sensor_data():
    """Broadcast sensor data to all connected clients"""
    while True:
        if clients:  # Only generate and send data if there are connected clients
            sensor_data = generate_sensor_data()
            # Send to all connected clients
            disconnected_clients = set()
            for client in clients:
                try:
                    client.send(json.dumps(sensor_data))
                except Exception as e:
                    print(f"Error sending to client: {e}")
                    disconnected_clients.add(client)

            # Remove disconnected clients
            clients.difference_update(disconnected_clients)

        time.sleep(10)  # Wait for 10 seconds before next update


# Start the broadcast thread
broadcast_thread = threading.Thread(target=broadcast_sensor_data, daemon=True)
broadcast_thread.start()


@app.route('/')
def index():
    return "WebSocket Server Running"


@sock.route('/ws')
def websocket(ws):
    """Handle WebSocket connections"""
    # Add this client to the set of connected clients
    clients.add(ws)

    # Send initial sensor data immediately upon connection
    initial_data = generate_sensor_data()
    ws.send(json.dumps(initial_data))

    try:
        # Keep the connection open and handle any incoming messages
        while True:
            message = ws.receive()
            if message is None:
                break

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        # Remove this client from the set of connected clients
        clients.remove(ws)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)