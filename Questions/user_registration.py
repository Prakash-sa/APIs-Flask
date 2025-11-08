import re
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash

app = Flask(__name__)

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
users = {}


def _validate_registration_payload(payload):
    errors = {}
    username = payload.get("username", "").strip()
    password = payload.get("password", "")
    email = payload.get("email", "").strip()

    if not username:
        errors["username"] = "username is required"
    elif username in users:
        errors["username"] = "username already exists"

    if len(password) < 6:
        errors["password"] = "password must be at least 6 characters"

    if not EMAIL_REGEX.match(email):
        errors["email"] = "a valid email address is required"

    return errors


@app.route("/register", methods=["POST"])
def register_user():
    payload = request.get_json(silent=True) or {}
    errors = _validate_registration_payload(payload)
    if errors:
        return jsonify(errors=errors), 400

    username = payload["username"].strip()
    users[username] = {
        "username": username,
        "email": payload["email"].strip(),
        "password_hash": generate_password_hash(payload["password"]),
    }
    return jsonify(message="User registered successfully", username=username), 201


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    user = users.get(username)
    if not user:
        return jsonify(error="User not found"), 404
    public_profile = {"username": user["username"], "email": user["email"]}
    return jsonify(public_profile)


if __name__ == "__main__":
    app.run(debug=True)
