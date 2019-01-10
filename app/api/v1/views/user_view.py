from flask import jsonify, request, abort, make_response
from ...v1 import version_1 as v1
from ..schemas.user_schema import UserSchema
from ..models.user_model import User
from ..models.token_model import RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                             get_jwt_identity, jwt_refresh_token_required, get_raw_jwt)

db = User()

@v1.route('/', methods=['GET'])
@v1.route('/index', methods=['GET'])
def index():
    return jsonify({'status': 200, 'message': 'Welcome to Questioner'}), 200

@v1.route('/register', methods=['POST'])
def register():
    """ Function to register new user """
    register_data = request.get_json()

    # No data has been provided
    if not register_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

    # Check if request is valid
    data, errors = UserSchema().load(register_data)
    if errors:
        abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors}), 400))

    # Check if username exists
    if db.exists('username', data['username']):
        abort(make_response(jsonify({'status': 409, 'message' : 'Username already exists'}), 409))

    # Check if email exists
    if db.exists('email', data['email']):
        abort(make_response(jsonify({'status': 409, 'message' : 'Email already exists'}), 409))

    # Save new user and get result
    new_user = db.save(data)
    result = UserSchema(exclude=['password']).dump(new_user).data

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

@v1.route('/login', methods=['POST'])
def login():
    """ Function to login existing user """
    login_data = request.get_json()

    # Check if request contains data
    if not login_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

    # Check if credentials have been passed
    data, errors = UserSchema().load(login_data, partial=True)
    if errors:
        abort(make_response(jsonify({'status': 400, 'message': 'Invalid data. Please fill all required fields', 'errors': errors}), 400))

    try:
        username = data['username']
        password = data['password']
    except:
        abort(make_response(jsonify({'status': 400, 'message': 'Invalid credentials'}), 400))

    # Check if username exists
    if not db.exists('username', username):
        abort(make_response(jsonify({'status': 404, 'message' : 'User not found'}), 404))

    user = db.find('username', username)

    # Check if password match
    db.checkpassword(user['password'], password)

     # Generate tokens and return response
    access_token = create_access_token(identity=user['id'], fresh=True)
    refresh_token = create_refresh_token(identity=True)
    return jsonify({
        'status': 200, 
        'message': 'User logged in successfully',
        'access_token': access_token,
        'refresh_token': refresh_token
        }), 200

@v1.route('/refresh-token', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    """ Endpoint to refresh user access token """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'status': 200, 'message': 'Token refreshed successfully', 'access_token': access_token})

@v1.route('logout', methods=['POST'])
@jwt_required
def logout():
    """ Endpoint to logout user """
    user_jti = get_raw_jwt()['jti']

    try:
        RevokedTokenModel().add(user_jti)
        return jsonify({'status': 200, 'message': 'Logged out successfully'}), 200
    except:
        abort(make_response(jsonify({"status": 500, "message": "Error deleting account"})))


