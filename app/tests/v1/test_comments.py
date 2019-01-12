from flask import json
from .base_test import BaseTest
from app.api.v1.models.comment_model import comments
from app.api.v1.models.question_model import questions

class TestComments(BaseTest):
    """ Test class for comments endpoints """

    def setUp(self):
        """ Initialize variables to be used for tests """
        super().setUp()

        self.meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }

        self.question = {
            'title' : 'Intro to python',
            'body' : 'Are we covering the basics?',
            'meetup' : 1,
            'created_by' : 4
        }

        self.comment = {
            'body' : 'Should include tests in the agenda too'
        }

        self.client.post('/api/v1/meetups', json=self.meetup)
        self.client.post('/api/v1/questions', json=self.question)

        self.headers = {'Content-Type': 'application/json'}

    def tearDown(self):
        """ Destroy initialized variables """
        comments.clear()
        questions.clear()
        super().tearDown()

    def test_post_comment_question_not_posted(self):
        """ Test post comment to a question that hasn't been posted """
        res = self.client.post('/api/v1/questions/3/comments')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Question not found')

    def test_post_comment_question_no_data(self):
        """ Test post comment without question data """
        res = self.client.post('/api/v1/questions/1/comments')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_comment_question_empty_data(self):
        """ Test post comment with empty data """
        # Clear comment
        self.comment.clear()

        res = self.client.post('/api/v1/questions/1/comments', json=json.dumps(self.comment), headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_post_comment(self):
        """ Test post comment successfully """
        res = self.client.post('/api/v1/questions/1/comments', json=self.comment, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Comment posted successfully')