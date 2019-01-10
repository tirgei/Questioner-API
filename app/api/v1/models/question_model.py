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

    def exists(self, key, value):
        """ Function to check if question with provided key, value exists """
        found_questions = [question for question in questions if value == question[key]]
        return len(found_questions) > 0 

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

        