from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def hello_plain():
    return "Hello, World"


@app.route("/hello-json", methods=["GET"])
def hello_json():
    return jsonify(message="Hey there! This is a JSON message!")


@app.route("/greet/<name>", methods=["GET"])
def greet(name):
    return jsonify(message=f"Greetings, {name}! Welcome to the dynamic route.")


@app.route("/greet/<first>/<last>", methods=["GET"])
def greet_full_name(first, last):
    return jsonify(message=f"Greetings, {first} {last}!")


@app.route("/route", methods=["GET"])
def read_query_parameter():
    variable = request.args.get("parameter_name", "default_value")
    return jsonify(parameter_name=variable)


@app.route("/greet", methods=["GET"])
def greet_name_age():
    name = request.args.get("name", "Guest")
    age = request.args.get("age", "unknown")
    return jsonify(message=f"Greetings, {name}! You are {age} years old.")


if __name__ == "__main__":
    app.run(debug=True)
