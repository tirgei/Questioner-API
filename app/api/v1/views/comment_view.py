from flask import Response, jsonify, request, make_response, abort
from ..schemas.comment_schema import CommentSchema
from ..models.comment_model import Comment as CommentModel
from ..models.question_model import Question
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource

db = CommentModel()
questions_db = Question()

class Comment(Resource):
    """ Resource for comments endpoints """

    @jwt_required
    def post(self, question_id):
        """ Endpoint to post comment to meetup question """

        message = ''
        status_code = 200
        response = {}

        comment_data = request.get_json()

        if not questions_db.exists('id', question_id):
            message = 'Question not found'
            status_code = 404

        elif not comment_data:
            message = 'No data provided'
            status_code = 400

        else: 
            try:
                data = CommentSchema().load(comment_data)

                data['user_id'] = get_jwt_identity()
                data['question_id'] = question_id
                comment = db.save(data)
                result = CommentSchema().dump(comment)

                status_code = 201
                message = 'Comment posted successfully'
                response.update({'data': result})

            except ValidationError as err:
                errors = err.messages

                status_code = 400
                message = 'Invalid data. Please fill all required fields'
                response.update({'errors': errors})

        response.update({'status': status_code, 'message': message})
        return response, status_code

    def get(self, question_id):
        """ Endpoint to fetch all comments for a question """

        status_code = 200
        response = {}

        if not questions_db.exists('id', question_id):
            status_code = 404
            response.update({'message': 'Question not found'})

        else:
            comments = db.all()
            result = CommentSchema(many=True).dump(comments)
            
            status_code = 200
            response.update({'data': result})

        response.update({'status': status_code})
        return response, status_code