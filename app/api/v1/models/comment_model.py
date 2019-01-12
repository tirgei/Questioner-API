from datetime import datetime
from .base_model import Model
from ..utils.utils import generate_id

comments = []

class Comment(Model):
    """ Model class for the Comment object """

    def __init__(self):
        super().__init__(comments)

    def save(self, data):
        """ Function to save new comment """
        data['id'] = generate_id(self.collection)
        return super().save(data)