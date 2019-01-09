from flask import jsonify, request
from ...v1 import version_1 as v1
from ..schemas.question_schema import QuestionSchema
from ..models.question_model import Question
from flask_jwt_extended import (jwt_required, get_jwt_identity)

db = Question()

@v1.route('/questions', methods=['POST'])
def post_question():
    """ Function to create meetup """
    json_data = request.get_json()

    # No data has been provided
    if not json_data:
        return jsonify({'status': 400, 'error': 'No data provided'}), 400

    # Check if request is valid
    data, errors = QuestionSchema().load(json_data)
    if errors:
        return jsonify({'status': 400, 'error' : 'Invalid data. Please fill all required fields', 'errors': errors}), 400

    # Save question and return response
    question = db.save(data)
    result = QuestionSchema().dump(question).data
    return jsonify({'status': 201, 'message': 'Question posted successfully', 'data': [result]}), 201