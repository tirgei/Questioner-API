from flask import jsonify, request, abort, make_response
from ...v1 import version_1 as v1
from ..schemas.meetup_schema import MeetupSchema
from ..models.meetup_model import Meetup
from marshmallow import ValidationError

db = Meetup()

@v1.route('/meetups', methods=['POST'])
def create_meetup():
    """ Endpoint to create meetup """
    json_data = request.get_json()

    # No data has been provided
    if not json_data:
        abort(make_response(jsonify({'status': 400, 'message': 'No data provided'}), 400))

    # Check if request is valid
    try:
        data = MeetupSchema().load(json_data)
    except ValidationError as errors:
        abort(make_response(jsonify({'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors.messages}), 400))

    # Save new meetup and return response
    new_meetup = db.save(data)
    result = MeetupSchema().dump(new_meetup)
    return jsonify({'status': 201, 'message': 'Meetup created successfully', 'data': [result]}), 201

@v1.route('/meetups/<int:meetup_id>', methods=['GET'])
def fetch_meetup(meetup_id):
    """ Endpoint to fetch specific meetup """
    # Check if meetup exists 
    if not db.exists('id', meetup_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Meetup not found'}), 404))

    # Get meetups 
    meetup = db.find('id', meetup_id)
    result = MeetupSchema().dump(meetup)
    return jsonify({'status':200, 'data':result}), 200

@v1.route('/meetups/upcoming', methods=['GET'])
def fetch_upcoming_meetups():
    """ Endpoint to fetch all meetups """
    meetups = db.all()
    result = MeetupSchema(many=True).dump(meetups)
    return jsonify({'status':200, 'data':result}), 200

@v1.route('/meetups', methods=['GET'])
def fetch_all_meetups():
    """ Endpoint to fetch all meetups """
    meetups = db.all()
    result = MeetupSchema(many=True).dump(meetups)
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
    
@v1.route('/meetups/<int:meetup_id>', methods=['DELETE'])
def delete_meetup(meetup_id):
    """ Endpoint to delete meetup """
    # Check if meetup exists 
    if not db.exists('id', meetup_id):
        abort(make_response(jsonify({'status': 404, 'message': 'Meetup not found'}), 404))

    # Get meetups 
    db.delete(meetup_id)
    return jsonify({'status':200, 'message': 'Meetup deleted successfully'}), 200