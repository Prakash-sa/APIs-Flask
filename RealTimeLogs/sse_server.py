from pathlib import Path
import sys

from flask import Flask, Response, jsonify, request, stream_with_context

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from log_reader import append_log_entry, follow_log  # noqa: E402

app = Flask(__name__)


def event_stream():
    for line in follow_log():
        yield f"data: {line}\n\n"


@app.route("/logs/events", methods=["GET"])
def stream_logs():
    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")


@app.route("/logs", methods=["POST"])
def add_log_entry():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message")
    if not message:
        return jsonify(error="message is required"), 400
    append_log_entry(message)
    return jsonify(status="queued"), 202


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
