from flask import jsonify, request, make_response
from ..schemas.meetup_schema import MeetupSchema
from ..models.meetup_model import Meetup as MeetupModel
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource

db = MeetupModel()

class Meetups(Resource):
    """ Resource for meetup endpoints """

    @jwt_required
    def post(self):
        """ Endpoint to create meetup """

        json_data = request.get_json()

        if not json_data:
            return {'status': 400, 'message': 'No data provided'}, 400

        try:
            data = MeetupSchema().load(json_data)
        except ValidationError as errors:
            return {'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors.messages}, 400

        data['user_id'] = get_jwt_identity()
        new_meetup = db.save(data)
        result = MeetupSchema().dump(new_meetup)
        return {'status': 201, 'message': 'Meetup created successfully', 'data': [result]}, 201

    def get(self):
        """ Endpoint to fetch all meetups """

        meetups = db.all()
        result = MeetupSchema(many=True).dump(meetups)
        return {'status':200, 'data':result}, 200

class Meetup(Resource):
    """ Resource for single meetup item """

    def get(self, meetup_id):
        """ Endpoint to fetch specific meetup """

        if not db.exists('id', meetup_id):
            return {'status': 404, 'message': 'Meetup not found'}, 404

        meetup = db.find('id', meetup_id)
        result = MeetupSchema().dump(meetup)
        return {'status':200, 'data':result}, 200

    @jwt_required
    def delete(self, meetup_id):
        """ Endpoint to delete meetup """

        if not db.exists('id', meetup_id):
            return {'status': 404, 'message': 'Meetup not found'}, 404

        db.delete(meetup_id)
        return {'status':200, 'message': 'Meetup deleted successfully'}, 200

class MeetupsUpcoming(Resource):
    """ Resource for upcoming meetups """

    def get(self):
        """ Endpoint to fetch all meetups """

        meetups = db.all()
        result = MeetupSchema(many=True).dump(meetups)
        return {'status':200, 'data':result}, 200

class MeetupRsvp(Resource):
    """ Resource for meetup rsvp """

    @jwt_required
    def post(self, meetup_id, rsvp):
        """ Endpoint to RSVP to meetup """
        valid_responses = ('yes', 'no', 'maybe')

        if not db.exists('id', meetup_id):
            return {'status': 404, 'message': 'Meetup not found'}, 404

        if rsvp not in valid_responses:
            return {'status': 400, 'message': 'Invalid rsvp'}, 400

        meetup = db.find('id', meetup_id)
        return {
            'status': 200,
            'message': 'Meetup rsvp successfully',
            'data': {
                'user_id': get_jwt_identity(),
                'meetup_id': meetup['id'],
                'topic' : meetup['topic'],
                'status': rsvp
            }
        }, 200