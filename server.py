from flask import Flask
from flask_socketio import SocketIO
import redis
import serial
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Configure the serial connection to STM32
ser = serial.Serial(
    port='/dev/ttyUSB0',  # Update this based on your STM32 connection
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


def process_lifi_data():
    while True:
        if ser.in_waiting > 0:
            try:
                # Read data from STM32
                data = ser.readline().decode('utf-8').strip()

                # Store in Redis
                redis_client.lpush('lifi_data', data)

                # Emit to connected clients
                socketio.emit('lifi_data', data)

            except Exception as e:
                print(f"Error processing data: {e}")


if __name__ == '__main__':
    # Start the background task for reading serial data
    socketio.start_background_task(process_lifi_data)

    # Run the server
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)