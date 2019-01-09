from flask import json
from .base_test import BaseTest

class TestQuestions(BaseTest):
    """ Test class for Questions endpoints """

    def setUp(self):
        """ Initialize variables to be used for tests """
        self.headers = {'Content-Type': 'application/json'}
        super().setUp()

    def post_question_no_data(self):
        """ Test post question with no data sent """
        res = self.client.post('/api/v1/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data provided')

    def test_post_question_empty_data(self):
        """ Test post question with no data sent """
        question = {}

        res = self.client.post('/api/v1/questions', json=json.dumps(question), headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Invalid data. Please fill all required fields')

    def test_post_question_missing_fields(self):
        """ Test post question with missing fields in data sent """
        # Question with no body
        question = {
            'title' : 'Intro to python'
        }

        res = self.client.post('/api/v1/questions', json=question, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Invalid data. Please fill all required fields')

    def test_post_question(self):
        """ Test post question successfully """
        question = {
            'title' : 'Intro to python',
            'body' : 'Are we covering the basics?',
            'meetup' : 2,
            'created_by' : 4
        }

        res = self.client.post('/api/v1/questions', json=question, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Question posted successfully')
    

