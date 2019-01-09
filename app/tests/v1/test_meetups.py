from flask import json
from .base_test import BaseTest

class TestMeetups(BaseTest):
    """ Test class for meetup endpoints """

    def setUp(self):
        """ Initialize variables to be used for tests """
        self.headers = {'Content-Type': 'application/json'}
        super().setUp()

    def test_create_meetup_no_data(self):
        """ Test create meetup with no data sent """
        res = self.client.post('/api/v1/meetups')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data provided')

    def test_create_meetup_empty_data(self):
        """ Test create meetup with no data sent """
        meetup = {}

        res = self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Invalid data. Please fill all required fields')

    def test_create_meetup_missing_fields(self):
        """ Test create meetup with missing fields in request """
        # Create meetup without location
        meetup = {
            'topic' : 'Leveling up with Python',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }

        res = self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Invalid data. Please fill all required fields')

    def test_create_meetup(self):
        """ Test create meetup successfully """
        meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }

        res = self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Meetup created successfully')
