from flask import jsonify, request, make_response
from ..schemas.question_schema import QuestionSchema
from ..models.question_model import Question as QuestionModel
from ..models.meetup_model import Meetup
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource

db = QuestionModel()
meetups_db = Meetup()

class Question(Resource):
    """ Resource for question endpoints """

    @jwt_required
    def post(self):
        """ Endpoint to post question """
        meetup_data = request.get_json()

        # No data has been provided
        if not meetup_data:
            return {'status': 400, 'message': 'No data provided'}, 400

        # Check if meetup exists
        try:
            meetup = meetup_data['meetup_id']
            if not meetups_db.exists('id', meetup):
                return {'status': 404, 'message': 'Meetup not found'}, 404
        except:
            return {'status': 404, 'message': 'Meetup not found'}, 404

        # Check if request is valid
        try:
            data = QuestionSchema().load(meetup_data)
        except ValidationError as errors:
            return {'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors.messages}, 400

        # Save question and return response
        data['user_id'] = get_jwt_identity()
        question = db.save(data)
        result = QuestionSchema().dump(question)
        return {'status': 201, 'message': 'Question posted successfully', 'data': result}, 201

class QuestionUpvote(Resource):
    """ Resource for upvoting question """

    def patch(self, question_id):
        """ Endpoint to upvote question """

        # Check if upvote question exists
        if not db.exists('id', question_id):
            return {'status': 404, 'message': 'Question not found'}, 404

        # Upvote question and return response
        question = db.upvote(question_id)
        result = QuestionSchema().dump(question)
        return {'status': 200, 'message': 'Question upvoted successfully', 'data': result}, 200

class QuestionDownvote(Resource):
    """ Resource for downvoting question """

    def patch(self, question_id):
        """ Endpoint to downvote question """

        # Check if downvote question exists
        if not db.exists('id', question_id):
            return {'status': 404, 'message': 'Question not found'}, 404

        # Upvote question and return response
        question = db.downvote(question_id)
        result = QuestionSchema().dump(question)
        return {'status': 200, 'message': 'Question downvoted successfully', 'data': result}, 200


class QuestionList(Resource):
    """ Resource for questions list """

    def get(self, meetup_id):
        """ Endpoint to fetch all questions for a specific meetup """

        # Check if meetup exists
        if not meetups_db.exists('id', meetup_id):
            return {'status': 404, 'message': 'Meetup not found'}, 404

        # Return list of questions
        questions = db.all()
        result = QuestionSchema(many=True).dump(questions)
        return {'status': 200, 'data': result}, 200
