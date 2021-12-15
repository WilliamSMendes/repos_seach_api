from flask import Flask, request 
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from user_schema import user_schema

app = Flask(__name__)

current_id = []
users = []

@app.route('/users', methods=['GET'])
def list_all_users():
    filtered_users = users
    filter_name = request.args.get('name', None)
    
    if filter_name:
        filtered_users = filter(lambda x: filter_name.lower() in x['name'].lower(), filtered_users)
    return {'users': users}

@app.route('/users', methods=['POST'])
def create_users():
    user = request.json

    try:
        validate(isntance=user, schema=user_schema)
    except ValidationError as e:
        return e.message, 400

    user['id'] = len(users) + 1
    users.append(user)
    return user

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(id):
    user = list(filter(lambda x: x['id'] == int(id), users))

    if not len(user):
        return 'User not found', 404

    user = user[0]
    update_request = request.json

    try:
        validate(isntance=update_request, schema=user_schema)
    except ValidationError as e:
        return e.message, 400

    for key in update_request:
        user[key] = update_request[key]

    return user

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(id):
    global users
    users = list(filter(lambda x: x['id'] != int(id), users))
    return {'message': 'User deleted'}