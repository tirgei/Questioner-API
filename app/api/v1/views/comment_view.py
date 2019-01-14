from flask import Response, jsonify, request, make_response
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

        comment_data = request.get_json()

        if not questions_db.exists('id', question_id):
            return {'status': 404, 'message': 'Question not found'}, 404

        if not comment_data:
            return {'status': 400, 'message': 'No data provided'}, 400

        try:
            data = CommentSchema().load(comment_data)
        except ValidationError as errors:
            return {'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors.messages}, 400

        data['user_id'] = get_jwt_identity()
        data['question_id'] = question_id
        comment = db.save(data)
        result = CommentSchema().dump(comment)
        return {'status': 201, 'message': 'Comment posted successfully', 'data': result}, 201

    def get(self, question_id):
        """ Endpoint to fetch all comments for a question """

        if not questions_db.exists('id', question_id):
            return {'status': 404, 'message': 'Question not found'}, 404

        comments = db.all()
        result = CommentSchema(many=True).dump(comments)
        return {'status': 200, 'data': result}, 200