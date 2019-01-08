from flask import jsonify, request
from ...v1 import version_1 as v1
from ..schemas.user_schema import UserSchema
from ..models.user_model import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)

db = User()

@v1.route('/', methods=['GET'])
@v1.route('/index', methods=['GET'])
def index():
    return jsonify({'status': 200, 'message': 'Welcome to Questioner'}), 200

@v1.route('/register', methods=['POST'])
def register():
    """ Function to register new user """
    json_data = request.get_json()

    # No data has been provided
    if not json_data:
        return jsonify({'status': 400, 'error': 'No data provided'}), 400

    # Check if request is valid
    data, errors = UserSchema().load(json_data)
    if errors:
        return jsonify({'status': 400, 'error' : 'Invalid data. Please fill all required fields', 'errors': errors}), 400

    # Check if username exists
    if db.exists('username', data['username']):
        return jsonify({'status': 409, 'error' : 'Username already exists'}), 409

    # Check if email exists
    if db.exists('email', data['email']):
        return jsonify({'status': 409, 'error' : 'Email already exists'}), 409

    # Save new user and get result
    new_user = db.save(data)
    result = UserSchema().dump(new_user).data

    # Generate access and refresh tokens and return response
    access_token = create_access_token(identity=new_user['id'], fresh=True)
    refresh_token = create_refresh_token(identity=new_user['id'])
    return jsonify({
        'status': 201, 
        'message' : 'User created successfully', 
        'data': result, 
        'access_token' : access_token, 
        'refresh_token' : refresh_token
        }), 201