from flask import Flask,jsonify,request,make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app=Flask(__name__)

limiter=Limiter(app,key_func=get_remote_address)

@app.route('/limited-access')
@limiter.limit("5 per minute")
def limited_access():
    return jsonify({'response':'This route is rate-limited'})

@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify{'error':'Rate limit exceeded'},429)

if __name__ == '__main__':
    app.run(debug=True)
    