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

        message = ''
        status_code = 200
        response = {}

        meetup_data = request.get_json()

        if not meetup_data:
            message = 'No data provided'
            status_code = 400

        else:
            try:
                meetup = meetup_data['meetup_id']
                
                if not meetups_db.exists('id', meetup):
                    message = 'Meetup not found'
                    status_code = 404

                else:
                    try:
                        data = QuestionSchema().load(meetup_data)

                        data['user_id'] = get_jwt_identity()
                        question = db.save(data)
                        result = QuestionSchema().dump(question)

                        status_code = 201
                        message = 'Question posted successfully'
                        response.update({'data': result})

                    except ValidationError as err:
                        errors = err.messages

                        status_code = 400
                        message = 'Invalid data. Please fill all required fields'
                        response.update({'errors': errors})

            except:
                message = 'Meetup not found'
                status_code = 404

        response.update({'status': status_code, 'message': message})
        return response, status_code

class QuestionUpvote(Resource):
    """ Resource for upvoting question """

    def patch(self, question_id):
        """ Endpoint to upvote question """

        message = ''
        status_code = 200
        response = {}

        if not db.exists('id', question_id):
            message = 'Question not found'
            status_code = 404

        else:
            question = db.upvote(question_id)
            result = QuestionSchema().dump(question)

            message = 'Question upvoted successfully'
            status_code = 200
            response.update({'data': result})

        response.update({'status': status_code, 'message': message})
        return response, status_code

class QuestionDownvote(Resource):
    """ Resource for downvoting question """

    def patch(self, question_id):
        """ Endpoint to downvote question """

        message = ''
        status_code = 200
        response = {}

        if not db.exists('id', question_id):
            message = 'Question not found'
            status_code = 404

        else:
            question = db.downvote(question_id)
            result = QuestionSchema().dump(question)

            message = 'Question downvoted successfully'
            status_code = 200
            response.update({'data': result})

        response.update({'status': status_code, 'message': message})
        return response, status_code


class QuestionList(Resource):
    """ Resource for questions list """

    def get(self, meetup_id):
        """ Endpoint to fetch all questions for a specific meetup """

        status_code = 200
        response = {}

        if not meetups_db.exists('id', meetup_id):
            status_code = 404
            response.update({'message': 'Meetup not found'})

        else:
            questions = db.all()
            result = QuestionSchema(many=True).dump(questions)
            response.update({'data': result})

        response.update({'status': status_code})
        return response, status_code
