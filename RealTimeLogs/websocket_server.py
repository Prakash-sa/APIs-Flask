import threading
from pathlib import Path
import sys

from flask import Flask, jsonify, request
from flask_socketio import SocketIO

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from log_reader import append_log_entry, follow_log  # noqa: E402

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")
_background_thread = None


def log_emitter():
    for line in follow_log():
        socketio.emit("log_entry", {"line": line})


def ensure_background_thread():
    global _background_thread
    if _background_thread is None:
        _background_thread = socketio.start_background_task(log_emitter)


@socketio.on("connect")
def on_connect():
    ensure_background_thread()
    socketio.emit("status", {"message": "connected"})


@app.route("/logs", methods=["POST"])
def add_log():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message")
    if not message:
        return jsonify(error="message is required"), 400
    append_log_entry(message)
    return jsonify(status="queued"), 202


if __name__ == "__main__":
    ensure_background_thread()
    socketio.run(app, debug=True)
