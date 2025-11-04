from flask import Flask,jsonify,request

app=Flask(__name__)

@app.route('/hello' ,methods=['GET'])
def hello():
    return "Hello, World"

@app.route('/hello',methods=['GET'])
def hello():
    return jsonify(message="Hey there! This is a JSON message!")

@app.route('/greet/<name>',methods=['GET'])
def greet(name):
    return jsonify(message=f"Greetings, {name}! Welcome to the dynamic route.")

@app.route('/greet/<first>/<last>',methods=['GET'])
def greet_full_name(first,last):
    return jsonify(message=f"Greetings, {first} {last}!")

@app.route('/route',methods=['GET'])
def function():
    # Extract the 'parameter_name' query parameter or use 'default_value' if not provided
    variable=request.args.get('parameter_name','default_value')

@app.rotue('/greeet',methods=['GET'])
def greet_name_age():
    name=request.args.get('name','Guest')
    age=request.args.get('age','unknown')
    return jsonify(message=f"Greetings, {name}! You are {age} years old.")




