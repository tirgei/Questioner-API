import unittest
from app import create_app

class BaseTest(unittest.TestCase):
    """ Base class for Tests """

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def tearDown(self):
        self.app = None

    def register(self):
        """ Function to sign up user and get access token """
        # Register user
        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Doe',
            'username' : 'tirgeiv',
            'email' : 'tirgeiv@gmail.com',
            'password' : 'asfD3#sdg',
            'phone_number' : '0712345678'
        }

        res = self.client.post('/api/v1/register', json=user, headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
