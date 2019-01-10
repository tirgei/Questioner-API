from flask import jsonify, request
from ...v1 import version_1 as v1
from ..schemas.question_schema import QuestionSchema
from ..models.question_model import Question
from flask_jwt_extended import (jwt_required, get_jwt_identity)

db = Question()

@v1.route('/questions', methods=['POST'])
def post_question():
    """ Endpoint to post question """
    meetup_data = request.get_json()

    # No data has been provided
    if not meetup_data:
        return jsonify({'status': 400, 'message': 'No data provided'}), 400

    # Check if request is valid
    data, errors = QuestionSchema().load(meetup_data)
    if errors:
        return jsonify({'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors}), 400

    # Save question and return response
    question = db.save(data)
    result = QuestionSchema().dump(question).data
    return jsonify({'status': 201, 'message': 'Question posted successfully', 'data': result}), 201

@v1.route('/questions/<int:question_id>/upvote', methods=['PATCH'])
def upvote_question(question_id):
    """ Endpoint to upvote question """

    # Check if question exists
    if not db.exists('id', question_id):
        return jsonify({'status': 404, 'message': 'Question not found'}), 404

    # Upvote question and return response
    question = db.upvote(question_id)
    result = QuestionSchema().dump(question).data
    return jsonify({'status': 200, 'message': 'Question upvoted successfully', 'data': result}), 200

@v1.route('/questions/<int:question_id>/downvote', methods=['PATCH'])
def downvote_question(question_id):
    """ Endpoint to downvote question """

    # Check if question exists
    if not db.exists('id', question_id):
        return jsonify({'status': 404, 'message': 'Question not found'}), 404

    # Upvote question and return response
    question = db.downvote(question_id)
    result = QuestionSchema().dump(question).data
    return jsonify({'status': 200, 'message': 'Question downvoted successfully', 'data': result}), 200

