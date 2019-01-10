from datetime import datetime
from ..utils.utils import generate_id
from .base_model import Model

meetups = []

class Meetup(Model):
    """ Model class for the meetup object """

    def __init__(self):
        super().__init__(meetups)

    def save(self, data):
        """ Function to save new meetup """
        data['id'] = generate_id(self.collection)
        return super().save(data)
