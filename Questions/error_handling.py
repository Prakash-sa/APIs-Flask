from flask import Flask, jsonify, make_response, request


class ValidationFailure(Exception):
    """Raised when a required query parameter is missing or invalid."""


class ResourceMissing(Exception):
    """Raised when the requested resource cannot be located."""


FAKE_DATASTORE = {
    1: {"id": 1, "name": "Interview Prep Checklist"},
    2: {"id": 2, "name": "Flask Best Practices"},
}

app = Flask(__name__)


@app.route("/items/<int:item_id>")
def get_item(item_id):
    try:
        if request.args.get("require_token") and request.args.get("token") != "secret":
            raise ValidationFailure("A valid token query parameter is required.")

        item = FAKE_DATASTORE.get(item_id)
        if item is None:
            raise ResourceMissing(f"Item with id={item_id} was not found.")

        return make_response(jsonify(result=item), 200)
    except ValidationFailure as exc:
        return make_response(jsonify(error=str(exc)), 400)
    except ResourceMissing as exc:
        return make_response(jsonify(error=str(exc)), 404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(error=getattr(error, "description", "Not Found")), 404)


@app.errorhandler(Exception)
def handle_unexpected(error):
    return make_response(jsonify(error="Internal server error"), 500)


if __name__ == "__main__":
    app.run(debug=True)
