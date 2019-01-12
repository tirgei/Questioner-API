from flask import jsonify, request, abort, make_response
from ...v1 import version_1 as v1
from ..schemas.comment_schema import CommentSchema
from ..models.comment_model import Comment
from ..models.question_model import Question
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

@v1.route('/questions/<int:question_id>/comments', methods=['GET'])
def fetch_all_comments(question_id):
    """ Endpoint to fetch all comments for a question """

    # Check if question exists
    if not questions_db.exists('id', question_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Question not found'}), 404))

    # Return list of comments
    comments = db.all()
    result = CommentSchema(many=True).dump(comments)
    return jsonify({'status': 200, 'data': result}), 200