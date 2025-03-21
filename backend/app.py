import os
import asyncio
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import logging
from data_fetcher import fetch_bitcoin_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Store active tasks to prevent duplicates
active_tasks = {}

@app.route('/')
def index():
    return "Flask-SocketIO server for Bitcoin On-Chain Signals is running."

async def background_task(sid):
    logger.info(f"Starting background task for client {sid}")
    while sid in active_tasks:
        try:
            data = fetch_bitcoin_data()
            if data:
                socketio.emit('update', data, to=sid)
                logger.info(f"Emitted data to client {sid}: {data}")
            else:
                socketio.emit('update', {'error': 'Failed to fetch data'}, to=sid)
                logger.error("Failed to fetch data")
        except Exception as e:
            socketio.emit('update', {'error': str(e)}, to=sid)
            logger.error(f"Error in background task for client {sid}: {e}")
        await asyncio.sleep(10)  # Wait for 10 seconds before the next update

@socketio.on('connect')
def handle_connect(auth=None):
    sid = request.sid
    logger.info(f"Client connected: {sid}")
    socketio.emit('start', to=sid)

@socketio.on('start')
def handle_start():
    sid = request.sid
    if sid not in active_tasks:
        logger.info(f"Starting background task for client {sid}")
        active_tasks[sid] = True
        socketio.start_background_task(lambda: asyncio.run(background_task(sid)))

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    logger.info(f"Client disconnected: {sid}")
    if sid in active_tasks:
        del active_tasks[sid]

if __name__ == '__main__':
    logger.info("Starting Flask-SocketIO server")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)