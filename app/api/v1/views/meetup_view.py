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

        message = ''
        status_code = 200
        response = {}

        json_data = request.get_json()

        if not json_data:
            message = 'No data provided'
            status_code = 400

        else:
            try:
                data = MeetupSchema().load(json_data)

                data['user_id'] = get_jwt_identity()
                new_meetup = db.save(data)
                result = MeetupSchema().dump(new_meetup)

                status_code = 201
                message = 'Meetup created successfully'

            except ValidationError as err:
                errors = err.messages

                status_code = 400
                message = 'Invalid data. Please fill all required fields'
                response.update({'errors': errors})

        response.update({'status': status_code, 'message': message})
        return response, status_code

    def get(self):
        """ Endpoint to fetch all meetups """

        meetups = db.all()
        result = MeetupSchema(many=True).dump(meetups)
        return {'status':200, 'data':result}, 200

class Meetup(Resource):
    """ Resource for single meetup item """

    def get(self, meetup_id):
        """ Endpoint to fetch specific meetup """

        status_code = 200
        response = {}

        if not db.exists('id', meetup_id):
            status_code = 404
            response.update({'message': 'Meetup not found'})

        else:
            meetup = db.find('id', meetup_id)
            result = MeetupSchema().dump(meetup)

            status_code = 200
            response.update({'data': result})

        response.update({'status': status_code})
        return response, status_code

    @jwt_required
    def delete(self, meetup_id):
        """ Endpoint to delete meetup """

        message = ''
        status_code = 200
        response = {}

        if not db.exists('id', meetup_id):
            status_code = 404
            message = 'Meetup not found'

        else:
            db.delete(meetup_id)

            status_code = 200
            message = 'Meetup deleted successfully'

        response.update({'status': status_code, 'message': message})
        return response, status_code

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

        message = ''
        status_code = 200
        response = {}

        valid_responses = ('yes', 'no', 'maybe')

        if not db.exists('id', meetup_id):
            print('Meetup not found')
            status_code = 404
            message = 'Meetup not found'

        elif rsvp not in valid_responses:
            status_code = 400
            message = 'Invalid rsvp'

        else:
            meetup = db.find('id', meetup_id)

            status_code = 200
            message = 'Meetup rsvp successfully'
            response.update({
                'data': {
                    'user_id': get_jwt_identity(),
                    'meetup_id': meetup['id'],
                    'topic' : meetup['topic'],
                    'status': rsvp
                }
            })

        response.update({'status': status_code, 'message': message})
        return response, status_code