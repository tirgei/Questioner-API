from flask import Flask, jsonify
from instance.config import app_config
from flask_jwt_extended import (JWTManager)
from app.api.v1 import version_1 

def create_app(config_name):
    """ Function to initialize Flask app """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    jwt = JWTManager(app)

    app.register_blueprint(version_1)

    @jwt.token_in_blacklist_loader
    def check_blacklisted(token):
        from app.api.v1.models.token_model import RevokedTokenModel
        jti = token['jti']
        return RevokedTokenModel().is_blacklisted(jti)

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

    return app