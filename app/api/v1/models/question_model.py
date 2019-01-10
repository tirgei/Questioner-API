from datetime import datetime
from .base_model import Model
from ..utils.utils import generate_id

questions = []

class Question(Model):
    """ Model class for the Question object """

    def __init__(self):
        super().__init__(questions)

    def save(self, data):
        """ Function to save new meetup """
        data['id'] = generate_id(self.collection)
        data['votes'] = 0
        return super().save(data)

    def upvote(self, question_id):
        """ Function to upvote question """
        for question in questions:
            if question['id'] == question_id:
                question['votes'] = question['votes']+1

            return question

    def downvote(self, question_id):
        """ Function to downvote question """
        for question in questions:
            if question['id'] == question_id:
                question['votes'] = question['votes']-1

            return question

        