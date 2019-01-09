from flask import jsonify, request
from ...v1 import version_1 as v1
from ..schemas.meetup_schema import MeetupSchema
from ..models.meetup_model import Meetup
from flask_jwt_extended import (jwt_required, get_jwt_identity)

db = Meetup()

@v1.route('/meetups', methods=['POST'])
def create_meetup():
    """ Function to create meetup """
    json_data = request.get_json()

    # No data has been provided
    if not json_data:
        return jsonify({'status': 400, 'error': 'No data provided'}), 400

    # Check if request is valid
    data, errors = MeetupSchema().load(json_data)
    if errors:
        return jsonify({'status': 400, 'error' : 'Invalid data. Please fill all required fields', 'errors': errors}), 400

    # Save new meetup and return response
    new_meetup = db.save(data)
    result = MeetupSchema().dump(new_meetup).data
    return jsonify({'status': 201, 'message': 'Meetup created successfully', 'data': [result]}), 201

@v1.route('/meetups/<int:meetup_id>', methods=['GET'])
def fetch_meetup(meetup_id):
    """ Function to fetch specific meetup """
    # Check if meetup exists 
    if not db.exists('id', meetup_id):
        return  jsonify({'status': 404, 'error': 'Meetup not found'}), 404

    # Get meetups 
    meetups = db.fetch_by_id(meetup_id)
    result = MeetupSchema(many=True).dump(meetups).data
    return jsonify({'status':200, 'data':result}), 200

@v1.route('/meetups/upcoming', methods=['GET'])
def fetch_upcoming_meetups():
    """ Function to fetch all meetups """
    meetups = db.all()
    result = MeetupSchema(many=True).dump(meetups).data
    return jsonify({'status':200, 'data':result}), 200