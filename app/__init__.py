from flask import Flask, jsonify
from instance.config import app_config
from flask_jwt_extended import (JWTManager)
from app.api.v1.views.user_view import v1 as users_blueprint_v1
from app.api.v1.views.meetup_view import v1 as meetups_blueprint_v1
from app.api.v1.views.question_view import v1 as questions_blueprint_v1
from app.api.v1.views.comment_view import v1 as comments_blueprint_v1

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
    app.register_blueprint(users_blueprint_v1)
    app.register_blueprint(meetups_blueprint_v1)
    app.register_blueprint(questions_blueprint_v1)
    app.register_blueprint(comments_blueprint_v1)

    @app.route('/')
    @app.route('/index')
    def index():
        return jsonify({'status': 200, 'message': 'Welcome to Questioner'})

    return app