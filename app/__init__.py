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
        """ Endpoint for the landing page """
        return jsonify({'status': 200, 'message': 'Welcome to Questioner'})

    @app.errorhandler(404)
    def page_not_found(error):
        """ Handler for error 404 """
        return jsonify({'status': 404, 'message': 'Oops! The requested page was not found'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """ Handler for error 405 """
        return jsonify({'status': 405, 'message': 'Method not allowed'}), 405

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        """ Handler for other error codes """
        return jsonify({'status': 500, 'message': 'Could not complete your request'}), 500

    return app