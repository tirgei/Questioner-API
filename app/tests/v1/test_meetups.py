from flask import json
from .base_test import BaseTest
from app.api.v1.models.meetup_model import meetups

class TestMeetups(BaseTest):
    """ Test class for meetup endpoints """

    def setUp(self):
        """ Initialize variables to be used for tests """
        super().setUp()

        self.meetup = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }

        self.meetup2 = {
            'topic' : 'Leveling up with Python',
            'location' : 'Andela HQ, Nairobi',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask']
        }

        self.meetup_no_location = {
            'topic' : 'Leveling up with Python',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask'],
        }

        self.meetup_empty_location = {
            'topic' : 'Leveling up with Python',
            'happening_on' : '08/01/2019',
            'tags' : ['python', 'flask'],
            'location' : ''
        }

        # Register user and get access_token
        super().register()
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

    def tearDown(self):
        """ Destroy initialized variables """
        meetups.clear()
        super().tearDown()

    def test_create_meetup_no_data(self):
        """ Test create meetup with no data sent """
        res = self.client.post('/api/v1/meetups', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_create_meetup_empty_data(self):
        """ Test create meetup with no data sent """
        meetup = {}

        res = self.client.post('/api/v1/meetups', json=json.dumps(meetup), headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_create_meetup_missing_fields(self):
        """ Test create meetup with missing fields in request """
        # Create meetup without location

        res = self.client.post('/api/v1/meetups', json=self.meetup_no_location, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_create_meetup_empty_fields(self):
        """ Test create meetup with empty fields in request """
        # Create meetup without location

        res = self.client.post('/api/v1/meetups', json=self.meetup_empty_location, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_create_meetup(self):
        """ Test create meetup successfully """
        res = self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Meetup created successfully')

    def test_fetch_specific_meetup(self):
        """ Test fetch a specific meetup using id """
        # Create meetups
        self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)
        self.client.post('/api/v1/meetups', json=self.meetup2, headers=self.headers)

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
        self.assertEqual(data['message'], 'Meetup not found')

    def test_fetch_all_upcoming_meetups(self):
        """ Test fetch all upcoming meetups """
        # Create meetups
        self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)
        self.client.post('/api/v1/meetups', json=self.meetup2, headers=self.headers)

        res = self.client.get('/api/v1/meetups/upcoming')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)

    def test_fetch_all_meetups(self):
        """ Test fetch all meetups """
        # Create meetups
        self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)
        self.client.post('/api/v1/meetups', json=self.meetup2, headers=self.headers)

        res = self.client.get('/api/v1/meetups')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)

    def test_rsvps_meetup_not_created(self):
        """ Test RSVP for meetup that hasn't been created """
        res = self.client.post('api/v1/meetups/3/yes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_rsvps_meetup_invalid_rsvp(self):
        """ Test RSVP for meetup that hasn't been created """
        self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)

        res = self.client.post('api/v1/meetups/1/attending', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid rsvp')

    def test_rsvps_yes(self):
        """ Test RSVPs yes to a meetup """
        self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)

        res = self.client.post('api/v1/meetups/1/yes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['status'], 'yes')

    def test_rsvps_no(self):
        """ Test RSVPs no to a meetup """
        self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)

        res = self.client.post('api/v1/meetups/1/no', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['status'], 'no')

    def test_rsvps_maybe(self):
        """ Test RSVPs yes to a meetup """
        self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)

        res = self.client.post('api/v1/meetups/1/maybe', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['status'], 'maybe')

    def test_delete_meetup_not_created(self):
        """ Test delete meetup hasn't been created """
        res = self.client.delete('api/v1/meetups/4', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_delete_meetup(self):
        """ Test delete meetup successfully """
        self.client.post('/api/v1/meetups', json=self.meetup, headers=self.headers)

        res = self.client.delete('api/v1/meetups/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup deleted successfully')