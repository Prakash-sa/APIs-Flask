from flask import Flask,request,jsonify

app=Flask(__name__)

@app.route('/v1/data')
def data_v1():
    return jsonify({'data':'Version 1 data'})

@app.route('/v2/data')
def data_v2():
    return jsonify({'data':'Version 2 data with additional features'})

if __name__=='__main__':
    app.run(debug=True)
