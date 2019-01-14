from flask import jsonify, request, make_response, Response, json
from ..schemas.user_schema import UserSchema
from ..models.user_model import User
from ..models.token_model import RevokedTokenModel
from marshmallow import ValidationError
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                             get_jwt_identity, jwt_refresh_token_required, get_raw_jwt)
from flask_restful import Resource

db = User()

class Index(Resource):
    """ Resource class for index """
    
    def get(self):
        return {'status': 200, 'message': 'Welcome to Questioner'}, 200

class Register(Resource):
    """ Resource class to register new user """

    def post(self):
        """ Endpoint to register user """
        register_data = request.get_json()

        # No data has been provided
        if not register_data:
            return {'status': 400, 'message': 'No data provided'}, 400

        # Check if request is valid
        try:
            data = UserSchema().load(register_data)
        except ValidationError as errors:
            return {'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors.messages}, 400

        # Check if username exists
        if next(filter(lambda u: u['username'] == data['username'], db.all()), None):
            return {'status': 409, 'message' : 'Username already exists'}, 409

        # Check if email exists
        if db.exists('email', data['email']):
            return {'status': 409, 'message' : 'Email already exists'}, 409

        # Save new user and get result
        new_user = db.save(data)
        result = UserSchema(exclude=['password']).dump(new_user)

        # Generate access and refresh tokens and return response
        access_token = create_access_token(identity=new_user['id'], fresh=True)
        refresh_token = create_refresh_token(identity=new_user['id'])
        return {
            'status': 201,
            'message' : 'User created successfully',
            'data': result,
            'access_token' : access_token,
            'refresh_token' : refresh_token
        }, 201

class Login(Resource):
    """ Resource class to login existing user """

    def post(self):
        """ Endpoint to login user """
        login_data = request.get_json()

        # Check if request contains data
        if not login_data:
            return {'status': 400, 'message': 'No data provided'}, 400

        # Check if credentials have been passed
        try:
            data = UserSchema().load(login_data, partial=True)
        except ValidationError as errors:
            return {'status': 400, 'message': 'Invalid data. Please fill all required fields', 'errors': errors.messages}, 400

        try:
            username = data['username']
            password = data['password']
        except:
            return {'status': 400, 'message': 'Invalid credentials'}, 400

        # Check if username exists
        if not db.exists('username', username):
            return {'status': 404, 'message' : 'User not found'}, 404

        user = db.find('username', username)

        # Check if password match
        db.checkpassword(user['password'], password)

        # Generate tokens and return response
        access_token = create_access_token(identity=user['id'], fresh=True)
        refresh_token = create_refresh_token(identity=True)
        return {
            'status': 200,
            'message': 'User logged in successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': user['id']
        }, 200

class RefreshToken(Resource):
    """ Resource class to refresh access token """

    @jwt_refresh_token_required
    def post(self):
        """ Endpoint to refresh user access token """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'status': 200, 'message': 'Token refreshed successfully', 'access_token': access_token}

class Logout(Resource):
    """ Resource class to logout user """

    @jwt_required
    def post(self):
        """ Endpoint to logout user """
        user_jti = get_raw_jwt()['jti']

        RevokedTokenModel().add(user_jti)
        return {'status': 200, 'message': 'Logged out successfully'}, 200


