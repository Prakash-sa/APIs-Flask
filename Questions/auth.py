from flask import Flask,request,jsonify
from functools import wraps

app=Flask(__name__)

users={"user1":"password1"}

def require_auth(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth=request.authorization
        if not auth or users.get(auth.username)!=auth.password:
            return jsonify({'message':'Authentication Required'}),401
        return f(*args,**kwargs)
    return decorated

@app.route('/secure_data')
@require_auth()
def secure_data():
    return jsonify({"message":"secure data accessed"})

if __name__=='__main__':
    app.run(debug=True)
