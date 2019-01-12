from flask import jsonify, request, abort, make_response
from ...v1 import version_1 as v1
from ..schemas.question_schema import QuestionSchema
from ..models.question_model import Question
from ..models.meetup_model import Meetup
from marshmallow import ValidationError

db = Question()
meetups_db = Meetup()

@v1.route('/questions', methods=['POST'])
def post_question():
    """ Endpoint to post question """
    meetup_data = request.get_json()

    # No data has been provided
    if not meetup_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

    # Check if meetup exists
    try:
        meetup = meetup_data['meetup']
        if not meetups_db.exists('id', meetup):
            abort(make_response(jsonify({'status': 404, 'message': 'Meetup not found'}), 404))
    except:
        abort(make_response(jsonify({'status': 404, 'message': 'Meetup not found'}), 404))

    # Check if request is valid
    try:
        data = QuestionSchema().load(meetup_data)
    except ValidationError as errors:
        abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors.messages}), 400))

    # Save question and return response
    question = db.save(data)
    result = QuestionSchema().dump(question)
    return jsonify({'status': 201, 'message': 'Question posted successfully', 'data': result}), 201

@v1.route('/questions/<int:question_id>/upvote', methods=['PATCH'])
def upvote_question(question_id):
    """ Endpoint to upvote question """

    # Check if upvote question exists
    if not db.exists('id', question_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Question not found'}), 404))

    # Upvote question and return response
    question = db.upvote(question_id)
    result = QuestionSchema().dump(question)
    return jsonify({'status': 200, 'message': 'Question upvoted successfully', 'data': result}), 200

@v1.route('/questions/<int:question_id>/downvote', methods=['PATCH'])
def downvote_question(question_id):
    """ Endpoint to downvote question """

    # Check if downvote question exists
    if not db.exists('id', question_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Question not found'}), 404))

    # Upvote question and return response
    question = db.downvote(question_id)
    result = QuestionSchema().dump(question)
    return jsonify({'status': 200, 'message': 'Question downvoted successfully', 'data': result}), 200

@v1.route('/meetups/<int:meetup_id>/questions', methods=['GET'])
def fetch_all_questions(meetup_id):
    """ Endpoint to fetch all questions for a specific meetup """

    # Check if meetup exists
    if not meetups_db.exists('id', meetup_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Meetup not found'}), 404))

    # Return list of questions
    questions = db.all()
    result = QuestionSchema(many=True).dump(questions)
    return jsonify({'status': 200, 'data': result}), 200
