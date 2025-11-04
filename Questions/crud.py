from flask import Flask,jsonify, request

app=Flask(__name__)
todos=[]

@app.route('/todos',methods=['GET','POST'])
def mangage_todo():
    if request.methods=='POST':
        todo=request.json
        todos.append(todo)
        return jsonify(todo),201

    return jsonify(todos)

@app.route('/todos/<int:todo_id>',methods=['DELETE','PUT'])
def update_delete_todo(todo_id):
    if request.methods=='PUT':
        for todo in todos:
            if todo['id']==todo_id:
                todo.update(request.json)
                return jsonify(todo)
        return jsonify({'error':'Not Found'}),404
    
    if request.methods=='DELETE':
        for i,todo in enumerate(todos):
            if todo['id']==todo_id:
                del todo[i]
                return jsonify({'result':'success'})
        return jsonify({'error':'Not Found'}),404

if __name__=="__main__":
    app.run(debug=True)
