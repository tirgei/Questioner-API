from flask import jsonify, request, abort, make_response
from ...v1 import version_1 as v1
from ..schemas.meetup_schema import MeetupSchema
from ..models.meetup_model import Meetup
from flask_jwt_extended import (jwt_required, get_jwt_identity)

db = Meetup()

@v1.route('/meetups', methods=['POST'])
def create_meetup():
    """ Endpoint to create meetup """
    json_data = request.get_json()

    # No data has been provided
    if not json_data:
        abort(make_response(jsonify({'status': 400, 'error': 'No data provided'}), 400))

    # Check if request is valid
    data, errors = MeetupSchema().load(json_data)
    if errors:
        abort(make_response(jsonify({'status': 400, 'error' : 'Invalid data. Please fill all required fields', 'errors': errors}), 400))

    # Save new meetup and return response
    new_meetup = db.save(data)
    result = MeetupSchema().dump(new_meetup).data
    return jsonify({'status': 201, 'message': 'Meetup created successfully', 'data': [result]}), 201

@v1.route('/meetups/<int:meetup_id>', methods=['GET'])
def fetch_meetup(meetup_id):
    """ Endpoint to fetch specific meetup """
    # Check if meetup exists 
    if not db.exists('id', meetup_id):
        abort(make_response(jsonify({'status': 404, 'error': 'Meetup not found'}), 404))

    # Get meetups 
    meetup = db.find('id', meetup_id)
    result = MeetupSchema().dump(meetup).data
    return jsonify({'status':200, 'data':result}), 200

@v1.route('/meetups/upcoming', methods=['GET'])
def fetch_upcoming_meetups():
    """ Endpoint to fetch all meetups """
    meetups = db.all()
    result = MeetupSchema(many=True).dump(meetups).data
    return jsonify({'status':200, 'data':result}), 200

@v1.route('/meetups/<int:meetup_id>/<string:rsvps>', methods=['POST'])
def rspvs_meetup(meetup_id, rsvps):
    """ Endpoint to RSVP to meetup """
    valid_responses = ('yes', 'no', 'maybe')

    # Check if meetup exists
    if not db.exists('id', meetup_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Meetup not found'}), 404))

    # Check if rsvp is valid
    if rsvps not in valid_responses:
        abort(make_response(jsonify({'status': 400, 'message': 'Invalid rsvp'}), 400))

    meetup = db.find('id', meetup_id)
    return jsonify({
        'status': 200,
        'message': 'Meetup rsvp successfully',
        'data': {
            'meetup': meetup['id'],
            'topic' : meetup['topic'],
            'status': rsvps
        }
    }), 200
    