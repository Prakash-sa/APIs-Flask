from flask import Flask, jsonify, request
from marshmallow import Schema, ValidationError, fields, validate, validates

database = [
    {
        "id": 1,
        "username": "cosmo",
        "email": "cosmo@example.com",
        "age": 30,
        "website": "https://example.com/cosmo",
        "address": {"street": "1 Galaxy Way", "city": "New York"},
    },
    {
        "id": 2,
        "username": "jake",
        "email": "jake@example.com",
        "age": 28,
        "website": "https://example.com/jake",
        "address": {"street": "23 Python Rd", "city": "Chicago"},
    },
]

app = Flask(__name__)


class AddressSchema(Schema):
    street = fields.Str(required=True)
    city = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Int(data_key="user_id")
    username = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True)
    age = fields.Int(validate=validate.Range(min=18, max=99))
    website = fields.Url(load_default=None)
    address = fields.Nested(AddressSchema, required=True)

    @validates("username")
    def validate_username(self, value):
        if not value.isalnum():
            raise ValidationError("Username must contain only letters and numbers.")

    @validates("email")
    def validate_email(self, value):
        if not value.endswith("@example.com"):
            raise ValidationError("Email must be an @example.com address.")


class ExampleSchema(Schema):
    example_field = fields.Str(required=True)

    @validates("example_field")
    def validate_example_field(self, value):
        if value != "expected_value":
            raise ValidationError("Value must be 'expected_value'.")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(users_schema.dump(database))


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((user for user in database if user["id"] == user_id), None)
    if user is None:
        return jsonify(error="User not found"), 404
    return jsonify(user_schema.dump(user))


@app.route("/users", methods=["POST"])
def create_user():
    try:
        user_data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(errors=err.messages), 400

    new_id = max(user["id"] for user in database) + 1 if database else 1
    user_data["id"] = new_id
    database.append(user_data)
    return jsonify(user_schema.dump(user_data)), 201


if __name__ == "__main__":
    app.run(debug=True)
