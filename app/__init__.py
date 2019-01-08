from flask import Flask
from instance.config import app_config
from flask_jwt_extended import (JWTManager)

def create_app(config_name):
    """ Function to initialize Flask app """

    # Initialize app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # Initialize JWT
    jwt = JWTManager(app)

    return app