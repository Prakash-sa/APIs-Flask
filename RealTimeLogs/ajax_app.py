from pathlib import Path
import sys

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from log_reader import append_log_entry, read_latest_lines  # noqa: E402

app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))


@app.route("/", methods=["GET"])
def index():
    return render_template("ajax_client.html")


@app.route("/logs/latest", methods=["GET"])
def latest_logs():
    return jsonify(entries=read_latest_lines(50))


@app.route("/logs", methods=["POST"])
def add_log():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message")
    if not message:
        return jsonify(error="message is required"), 400
    append_log_entry(message)
    return jsonify(status="queued"), 202


if __name__ == "__main__":
    app.run(debug=True)
