from flask import json
from .base_test import BaseTest
from app.api.v1.models.meetup_model import meetups

class TestMeetups(BaseTest):
    """ Test class for meetup endpoints """

    def setUp(self):
        """ Initialize variables to be used for tests """
        self.headers = {'Content-Type': 'application/json'}
        super().setUp()

    def tearDown(self):
        """ Desdtroy initialized variables """
        meetups.clear()
        super().tearDown()

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

        res = self.client.post('/api/v1/meetups', json=json.dumps(meetup), headers=self.headers)
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

    def test_fetch_specific_meetup(self):
        """ Test fetch a specific meetup using id """
        # Create meetups
        meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }
        meetup2 = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }
        self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)
        self.client.post('/api/v1/meetups', json=meetup2, headers=self.headers)

        res = self.client.get('/api/v1/meetups/1')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['data']['id'], 1)

    def test_fetch_non_existent_meetup(self):
        """ Test fetch a non existing meetup """
        res = self.client.get('/api/v1/meetups/10')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Meetup not found')

    def test_fetch_all_meetups(self):
        """ Test fetch all meetups """
        # Create meetups
        meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }
        meetup2 = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }
        self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)
        self.client.post('/api/v1/meetups', json=meetup2, headers=self.headers)

        res = self.client.get('/api/v1/meetups/upcoming')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)

    def test_rsvps_meetup_not_created(self):
        """ Test RSVP for meetup that hasn't been created """
        res = self.client.post('api/v1/meetups/3/yes')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_rsvps_meetup_invalid_rsvp(self):
        """ Test RSVP for meetup that hasn't been created """
        meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }
        self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)

        res = self.client.post('api/v1/meetups/1/attending')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid rsvp')

    def test_rsvps_yes(self):
        """ Test RSVPs yes to a meetup """
        meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }
        self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)

        res = self.client.post('api/v1/meetups/1/yes')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['status'], 'yes')

    def test_rsvps_no(self):
        """ Test RSVPs no to a meetup """
        meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }
        self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)

        res = self.client.post('api/v1/meetups/1/no')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['status'], 'no')

    def test_rsvps_maybe(self):
        """ Test RSVPs yes to a meetup """
        meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }
        self.client.post('/api/v1/meetups', json=meetup, headers=self.headers)

        res = self.client.post('api/v1/meetups/1/maybe')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['status'], 'maybe')
