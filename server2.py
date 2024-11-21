from flask import Flask, request
from flask_cors import CORS
from flask_sock import Sock
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
sock = Sock(app)

# Store connected clients
clients = set()


@app.route('/')
def index():
    return "WebSocket Server Running"


@sock.route('/ws')
def websocket(ws):
    """Handle WebSocket connections"""
    # Add this client to the set of connected clients
    clients.add(ws)
    print(f"Client connected. Total clients: {len(clients)}")
    # Send a connection message
    welcome_message = {
        'type': 'system',
        'content': 'Connected to server',
        'time': datetime.now().strftime('%H:%M:%S')
    }
    ws.send(json.dumps(welcome_message))

    try:
        # Keep the connection open and listen for messages
        while True:
            message = ws.receive()
            print(f"Received message: {message}")
            if message:
                # Parse the incoming message
                try:
                    parsed_message = json.loads(message)

                    # Broadcast the message to all connected clients
                    broadcast_message = {
                        'type': parsed_message.get('type', 'user'),
                        'content': parsed_message.get('content', ''),
                        'time': datetime.now().strftime('%H:%M:%S')
                    }

                    # Send to all connected clients
                    for client in clients:
                        client.send(json.dumps(broadcast_message))

                except json.JSONDecodeError:
                    print("Invalid message format")

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        # Remove this client from the set of connected clients
        clients.remove(ws)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)