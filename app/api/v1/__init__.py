""" Initiates blueprints for version 1 of the API """
from flask import Blueprint

version_1 = Blueprint('version_one', __name__, url_prefix='/api/v1')