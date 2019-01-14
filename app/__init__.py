from flask import Flask, jsonify
from instance.config import app_config
from flask_jwt_extended import (JWTManager)
from app.api.v1 import version_1 

def create_app(config_name):
    """ Function to initialize Flask app """

    # Initialize app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # Initialize JWT
    jwt = JWTManager(app)
    @jwt.token_in_blacklist_loader
    def check_blacklisted(token):
        from app.api.v1.models.token_model import RevokedTokenModel
        jti = token['jti']
        return RevokedTokenModel().is_blacklisted(jti)

    # Register V1 Blueprints
    app.register_blueprint(version_1)

    @app.route('/')
    @app.route('/index')
    def index():
        return jsonify({'status': 200, 'message': 'Welcome to Questioner'})

    return app