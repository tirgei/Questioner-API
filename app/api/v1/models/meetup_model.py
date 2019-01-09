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