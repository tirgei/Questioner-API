from flask import jsonify, request, abort, make_response
from ...v1 import version_1 as v1
from ..schemas.comment_schema import CommentSchema
from ..models.comment_model import Comment
from ..models.question_model import Question
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from marshmallow import ValidationError

db = Comment()
questions_db = Question()

@v1.route('/questions/<int:question_id>/comments', methods=['POST'])
def post_comment(question_id):
    """ Endpoint to post comment to meetup question """
    comment_data = request.get_json()

    # Check if question exists
    if not questions_db.exists('id', question_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Question not found'}), 404))

    # Check if data exists
    if not comment_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

    # Check if request is valid
    try:
        data = CommentSchema().load(comment_data)
    except ValidationError as errors:
        abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors.messages}), 400))

    # Save question and return response
    comment = db.save(data)
    result = CommentSchema().dump(comment)
    return jsonify({'status': 201, 'message': 'Comment posted successfully', 'data': result}), 201


