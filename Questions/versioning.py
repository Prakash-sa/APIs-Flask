from flask import Blueprint, Flask, jsonify

app = Flask(__name__)

v1 = Blueprint("v1", __name__, url_prefix="/v1")
v2 = Blueprint("v2", __name__, url_prefix="/v2")


@v1.route("/data", methods=["GET"])
def data_v1():
    return jsonify(data="Version 1 data")


@v2.route("/data", methods=["GET"])
def data_v2():
    return jsonify(data="Version 2 data with additional features")


app.register_blueprint(v1)
app.register_blueprint(v2)


if __name__ == "__main__":
    app.run(debug=True)
