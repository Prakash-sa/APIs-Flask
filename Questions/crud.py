from flask import Flask, jsonify, request

app = Flask(__name__)

todos = [
    {"id": 1, "title": "Draft interview prep notes", "done": False},
    {"id": 2, "title": "Review Flask CRUD patterns", "done": True},
]


def _find_todo(todo_id):
    return next((todo for todo in todos if todo["id"] == todo_id), None)


@app.route("/todos", methods=["GET", "POST"])
def manage_todos():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        title = payload.get("title")
        if not title:
            return jsonify(error="title is required"), 400

        new_id = max(todo["id"] for todo in todos) + 1 if todos else 1
        todo = {"id": new_id, "title": title, "done": bool(payload.get("done", False))}
        todos.append(todo)
        return jsonify(todo), 201

    return jsonify(todos)


@app.route("/todos/<int:todo_id>", methods=["GET", "PUT", "DELETE"])
def todo_detail(todo_id):
    todo = _find_todo(todo_id)
    if todo is None:
        return jsonify(error="Not Found"), 404

    if request.method == "GET":
        return jsonify(todo)

    if request.method == "PUT":
        payload = request.get_json(silent=True) or {}
        todo["title"] = payload.get("title", todo["title"])
        if "done" in payload:
            todo["done"] = bool(payload["done"])
        return jsonify(todo)

    todos.remove(todo)
    return jsonify(result="success")


if __name__ == "__main__":
    app.run(debug=True)
