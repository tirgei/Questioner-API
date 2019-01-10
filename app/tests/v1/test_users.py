from flask import json
from .base_test import BaseTest
from app.api.v1.models.user_model import users

class TestUser(BaseTest):
    """ Test class for user endpoints """

    def setUp(self):
        """ Initialize variables to be used for user tests """
        super().setUp()

    def tearDown(self):
        """ Destroy initialized variables """
        users.clear()
        super().tearDown()

    def test_index(self):
        """ Test index """
        res = self.client.get('/api/v1/index')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Welcome to Questioner')

    def test_signup_no_data(self):
        """ Test sign up with no data sent """
        res = self.client.post('/api/v1/register')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_signup_empty_data(self):
        """ Test sign up with empty data sent """
        user = {}

        res = self.client.post('/api/v1/register', json=json.dumps(user), headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup_missing_fields(self):
        """ Test signup with missing fields in data sent """
        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'password' : 'asfsgsdg'
        }

        res = self.client.post('/api/v1/register', json=user, headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup_invalid_email(self):
        """ Test sign up with invalid email """

        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Doe',
            'username' : 'tirgei',
            'email' : 'tirgei',
            'password' : 'asfsgsdg',
            'phone_number' : '0712345678'
        }

        res = self.client.post('/api/v1/register', json=user, headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup_invalid_password(self):
        """ Test signup with invalid password """

        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Doe',
            'username' : 'tirgei',
            'email' : 'tirgei@gmail.com',
            'password' : 'asfsgsdg',
            'phone_number' : '0712345678'
        }

        res = self.client.post('/api/v1/register', json=user, headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup(self):
        """ Test sign up with correct data """

        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Doe',
            'username' : 'tirgei',
            'email' : 'tirgei@gmail.com',
            'password' : 'asfD3#sdg',
            'phone_number' : '0712345678'
        }

        res = self.client.post('/api/v1/register', json=user, headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'User created successfully')
        self.assertEqual(data['data']['username'], user['username'])

    def test_signup_existing_email(self):
        """ Test sign up with existing email """

        # Create new user and test response
        user_1 = {
            'firstname' : 'John',
            'lastname' : 'Doe',
            'othername' : 'Oketch',
            'username' : 'joketch',
            'email' : 'jd@gmail.com',
            'password' : 'asfD3#sdg',
            'phone_number' : '0712345678'
        }

        res_1 = self.client.post('/api/v1/register', json=user_1, headers={'Content-Type': 'application/json'})
        data_1 = res_1.get_json()

        self.assertEqual(res_1.status_code, 201)
        self.assertEqual(data_1['status'], 201)

        # Create another user with same email
        user_2 = {
            'firstname' : 'Jane',
            'lastname' : 'Dilly',
            'othername' : 'Dudley',
            'username' : 'dilly',
            'email' : 'jd@gmail.com',
            'password' : 'asfD3#sdg',
            'phone_number' : '0712345678'
        }

        res_2 = self.client.post('/api/v1/register', json=user_2, headers={'Content-Type': 'application/json'})
        data_2 = res_2.get_json()

        self.assertEqual(res_2.status_code, 409)
        self.assertEqual(data_2['status'], 409)
        self.assertEqual(data_2['message'], 'Email already exists')

    def test_signup_existing_username(self):
        """ Test sign up with existing username """

        # Create new user and test response
        user_1 = {
            'firstname' : 'John',
            'lastname' : 'Doe',
            'othername' : 'Oketch',
            'username' : 'doe',
            'email' : 'john@gmail.com',
            'password' : 'asfD3#sdg',
            'phone_number' : '0712345678'
        }

        res_1 = self.client.post('/api/v1/register', json=user_1, headers={'Content-Type': 'application/json'})
        data_1 = res_1.get_json()

        self.assertEqual(res_1.status_code, 201)
        self.assertEqual(data_1['status'], 201)

        # Create another user with same email
        user_2 = {
            'firstname' : 'Jane',
            'lastname' : 'Dilly',
            'othername' : 'Dudley',
            'username' : 'doe',
            'email' : 'jdoe@gmail.com',
            'password' : 'asfD3#sdg',
            'phone_number' : '0712345678'
        }

        res_2 = self.client.post('/api/v1/register', json=user_2, headers={'Content-Type': 'application/json'})
        data_2 = res_2.get_json()

        self.assertEqual(res_2.status_code, 409)
        self.assertEqual(data_2['status'], 409)
        self.assertEqual(data_2['message'], 'Username already exists')

    def test_login_no_data(self):
        """ Test login with no data provided """
        res = self.client.post('/api/v1/login')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_login_empty_data(self):
        """ Test login with empty data provided """
        user = {}

        res = self.client.post('/api/v1/login', json=user, headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_login_unregistered_user(self):
        """ Test login with unregistered user credentials """
        user = {
            'username' : 'mikey',
            'password' : 'sfsf87#E'
        }

        res = self.client.post('/api/v1/login', json=user, headers={'Content-Type': 'application/json'})
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'User not found')

    def test_login(self):
        """ Test successfull login """
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

        res_1 = self.client.post('/api/v1/register', json=user, headers={'Content-Type': 'application/json'})
        data_1 = res_1.get_json()

        self.assertEqual(res_1.status_code, 201)
        self.assertEqual(data_1['status'], 201)

        # Login user
        res_2 = self.client.post('/api/v1/login', json={'username': 'tirgeiv', 'password': 'asfD3#sdg'}, headers={'Content-Type': 'application/json'})
        data_2 = res_2.get_json()

        self.assertEqual(res_2.status_code, 200)
        self.assertEqual(data_2['status'], 200)
        self.assertEqual(data_2['message'], 'User logged in successfully')

    def test_login_no_username_provided(self):
        """ Test login with no username provided """
        # Register user
        user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Doe',
            'username' : 'tirgeic',
            'email' : 'tirgeic@gmail.com',
            'password' : 'asfD3#sdg',
            'phone_number' : '0712345678'
        }

        res_1 = self.client.post('/api/v1/register', json=user, headers={'Content-Type': 'application/json'})
        data_1 = res_1.get_json()

        self.assertEqual(res_1.status_code, 201)
        self.assertEqual(data_1['status'], 201)

        # Login user
        res_2 = self.client.post('/api/v1/login', json={'password': 'asfD3#sdg'}, headers={'Content-Type': 'application/json'})
        data_2 = res_2.get_json()

        self.assertEqual(res_2.status_code, 400)
        self.assertEqual(data_2['status'], 400)
        self.assertEqual(data_2['message'], 'Invalid credentials')

    def test_refresh_access_token_no_token_passed(self):
        """ Test refresh access token without passing refresh token"""

        res = self.client.post('/api/v1/refresh-token')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)

    def test_refresh_access_token_passing_access_token(self):
        """ Test refresh access token passing access token """
        self.__register()

        res = self.client.post('/api/v1/refresh-token', headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['msg'], 'Only refresh tokens are allowed')


    def test_refresh_access_token(self):
        """ Test refresh access token """
        self.__register()

        res = self.client.post('/api/v1/refresh-token', headers={'Authorization': 'Bearer {}'.format(self.refresh_token)})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Token refreshed successfully')


    def __register(self):
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
    



    