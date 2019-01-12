from flask import json
from .base_test import BaseTest
from app.api.v1.models.question_model import questions

class TestQuestions(BaseTest):
    """ Test class for Questions endpoints """

    def setUp(self):
        """ Initialize variables to be used for tests """
        super().setUp()

        self.question_empty = {}

        self.question = {
            'title' : 'Intro to python',
            'body' : 'Are we covering the basics?',
            'meetup' : 2,
            'created_by' : 4
        }

        self.question_incomplete = {
            'title' : 'Intro to python'
        }

        self.headers = {'Content-Type': 'application/json'}

    def tearDown(self):
        """ Destroy initialized variables after test """
        questions.clear()
        super().tearDown()

    def post_question_no_data(self):
        """ Test post question with no data sent """
        res = self.client.post('/api/v1/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_question_empty_data(self):
        """ Test post question with no data sent """
        res = self.client.post('/api/v1/questions', json=json.dumps(self.question_empty), headers = self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_post_question_missing_fields(self):
        """ Test post question with missing fields in data sent """
        # Question with no body
        res = self.client.post('/api/v1/questions', json=self.question_incomplete, headers = self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_post_question(self):
        """ Test post question successfully """
        res = self.client.post('/api/v1/questions', json=self.question, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Question posted successfully')

    def test_upvote_question_not_posted(self):
        """ Test upvote for question that hasn't been posted """
        res = self.client.patch('/api/v1/questions/3/upvote')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Question not found')

    def test_upvote_question(self):
        """ Test upvote question successfully """
        res_post = self.client.post('/api/v1/questions', json=self.question, headers=self.headers)
        question_id = res_post.get_json()['data']['id']

        res = self.client.patch('/api/v1/questions/{}/upvote'.format(question_id))
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Question upvoted successfully')
        self.assertEqual(data['data']['votes'], 1)

    def test_downvote_question_not_posted(self):
        """ Test downvote for question that hasn't been posted """
        res = self.client.patch('/api/v1/questions/3/downvote')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Question not found')

    def test_downvote_question(self):
        """ Test downvote question successfully """
        self.client.post('/api/v1/questions', json=self.question, headers=self.headers)

        res = self.client.patch('/api/v1/questions/1/downvote')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Question downvoted successfully')
        self.assertEqual(data['data']['votes'], -1)

