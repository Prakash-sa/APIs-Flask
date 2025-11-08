from flask import Flask, request, jsonify, make_response
from functools import wraps

app = Flask(__name__)

users = {"user1": "password1"}

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or users.get(auth.username) != auth.password:
            response = jsonify(message="Authentication Required")
            return make_response(response, 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})
        return f(*args, **kwargs)

    return decorated


@app.route("/secure_data")
@require_auth
def secure_data():
    return jsonify(message="secure data accessed")


if __name__ == "__main__":
    app.run(debug=True)
