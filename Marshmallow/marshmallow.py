from marshmallow import Schema,fields,ValidationError,validate,validates
from flask import Flask,request,jsonify

database = [
    {"id": 1, "username": "cosmo", "email": "cosmo@example.com"},
    {"id": 2, "username": "jake", "email": "jake@example.com"},
    {"id": 3, "username": "emma", "email": "emma@example.com"}
]

app=Flask(__name__)

class AddressSchema(Schema):
    street=fields.Str(required=True)
    city=fields.Str(required=True)

class UserSchema(Schema):
    id=fields.Int(data_key='user_id')
    username=fields.Str(required=True, validate=validate.Length(min=3,max=20))
    email=fields.Email(required=True)
    age=fields.Int(validate=validate.Range(min=18,max=99))
    website=fields.Url()
    address=fields.Nested(AddressSchema,required=True)

    @validates('username')
    def validate_username(self,value):
        if len(value)<3:
            raise ValidationError('Username must be at least 3 characters.')
        if not value.isalnum():
            raise ValidationError('Username must contain only letters and numbers')

    @validates('email')
    def validate_email(self,value):
        if not value.endswith('@example.com'):
            raise ValidationError('Email must be valid @example.com address.')
    
    @validate('email')
    def validate_email(self,value):
        if not value.endswith('@example.com'):
            raise ValidationError('Email must be valid @')


class ExampleSchema(Schema):
    example_field=fields.Str()

    @validates('example_field')
    def validate_example_field(self,value):
        if value!='expected_value':
            raise ValidationError('Value must be ...')


user_schema=UserSchema()

@app.route('/users/<int>')
def get_user(user_id):
    user=next((user for user in database if user['id']==user_id),None)
    if user is None:
        return jsonify(error='User not found'),404
    
    result=user_schema.dump(user)
    return jsonify(result)

@app.route('/users',methods=['POST'])
def create_user():
    try:
        user_data=user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(error=err.messages),400
    
    new_id=max(user['id'] for user in database)+1
    user_data['id']=new_id
    database.append(user_data)
    return jsonify(new_user),201


