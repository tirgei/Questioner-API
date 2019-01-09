from datetime import datetime
from ..utils.utils import generate_id

questions = []

class Question(object):
    """ Model class for the Question object """

    def save(self, data):
        """ Function to save new meetup """
        data['id'] = generate_id(questions)
        data['created_on'] = datetime.now()
        data['modified_on'] = datetime.now()
        data['votes'] = 0
        questions.append(data)
        return data