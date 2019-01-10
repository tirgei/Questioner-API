from datetime import datetime
from ..utils.utils import generate_id

meetups = []

class Meetup(object):
    """ Model class for the meetup object """

    def save(self, data):
        """ Function to save new meetup """
        data['id'] = generate_id(meetups)
        data['created_on'] = datetime.now()
        data['modified_on'] = datetime.now()
        meetups.append(data)
        return data

    def fetch_by_id(self, id):
        """ Function to fetch meetups by ID """
        fetched_meetups = [meetup for meetup in meetups if meetup['id'] == id]
        return fetched_meetups[0]

    def exists(self, key, value):
        """ Function to check if meetup exists """
        fetched_meetups = [meetup for meetup in meetups if meetup[key] == value]
        return len(fetched_meetups) > 0

    def all(self):
        """ Function to fetch all meetups """
        return meetups