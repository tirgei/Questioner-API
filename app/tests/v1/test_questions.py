from flask import json
from .base_test import BaseTest
from app.api.v1.models.question_model import questions

class TestQuestions(BaseTest):
    """ Test class for Questions endpoints """

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

        self.question_2 = {
            'title' : 'Flask',
            'body' : 'Are we doing an API?',
            'meetup' : 1,
            'created_by' : 4
        }

        self.client.post('/api/v1/meetups', json=self.meetup)

        self.headers = {'Content-Type': 'application/json'}

    def tearDown(self):
        """ Destroy initialized variables after test """
        questions.clear()
        super().tearDown()

    def test_post_question_meetup_not_created(self):
        """ Test post question to meetup that doesn't exist """
        # Assign question meetup id that doesn't exist
        self.question.update({'meetup': 11})

        res = self.client.post('/api/v1/questions', json=self.question)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_post_question_without_meetup_id(self):
        """ Test post question to meetup that doesn't exist """
        # Remove meetup id
        self.question.pop('meetup', None)

        res = self.client.post('/api/v1/questions', json=self.question)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def post_question_no_data(self):
        """ Test post question with no data sent """
        res = self.client.post('/api/v1/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_question_empty_data(self):
        """ Test post question with no data sent """
        # Clear question
        self.question.clear()

        res = self.client.post('/api/v1/questions', json=self.question)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_question_missing_fields(self):
        """ Test post question with missing fields in data sent """
        # Remove body from question
        self.question.pop('body', None)

        res = self.client.post('/api/v1/questions', json=self.question)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_post_question(self):
        """ Test post question successfully """
        res = self.client.post('/api/v1/questions', json=self.question)
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
        self.client.post('/api/v1/questions', json=self.question)

        res = self.client.patch('/api/v1/questions/1/upvote')
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
        self.client.post('/api/v1/questions', json=self.question)

        res = self.client.patch('/api/v1/questions/1/downvote')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Question downvoted successfully')
        self.assertEqual(data['data']['votes'], -1)

    def test_fetch_all_questions_meetup_not_created(self):
        """ Test fetch all questions for a meetup that doesn't exist """
        res = self.client.get('/api/v1/meetups/13/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_fetch_all_questions(self):
        """ Test fetch all questions for a meetup """
        self.client.post('/api/v1/questions', json=self.question)
        self.client.post('/api/v1/questions', json=self.question_2)

        res = self.client.get('/api/v1/meetups/1/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)

