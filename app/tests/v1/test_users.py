from flask import json
from .base_test import BaseTest
from app.api.v1.models.user_model import users

class TestUser(BaseTest):
    """ Test class for user endpoints """

    def setUp(self):
        """ Initialize variables to be used for user tests """

        super().setUp()

        self.user = {
            'firstname' : 'Vincent',
            'lastname' : 'Tirgei',
            'othername' : 'Kip',
            'username' : 'tirgeiv',
            'email' : 'tirgeiv@gmail.com',
            'password' : 'asfD3#sdg',
            'phone_number' : '0712345678'
        }

        super().register()

        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}


    def tearDown(self):
        """ Destroy initialized variables """

        users.clear()
        super().tearDown()

    def test_landing(self):
        """ Test landing endpoint """

        res = self.client.get('/index')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Welcome to Questioner')

    def test_index(self):
        """ Test index """

        res = self.client.get('/api/v1/')
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

        self.user.clear()
        
        res = self.client.post('/api/v1/register', json=json.dumps(self.user))
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup_missing_fields(self):
        """ Test signup with missing fields in data sent """

        self.user.pop('username', None)

        res = self.client.post('/api/v1/register', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup_invalid_email(self):
        """ Test sign up with invalid email """

        self.user.update({'email': 'tirgeic'})

        res = self.client.post('/api/v1/register', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup_invalid_password(self):
        """ Test signup with invalid password """

        self.user.update({'password': 'afsdgdfhd'})

        res = self.client.post('/api/v1/register', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup_short_password(self):
        """ Test signup with short password """

        self.user.update({'password': 'asad'})

        res = self.client.post('/api/v1/register', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_signup(self):
        """ Test sign up with correct data """

        res = self.client.post('/api/v1/register', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'User created successfully')
        self.assertEqual(data['data']['username'], self.user['username'])

    def test_signup_existing_email(self):
        """ Test sign up with existing email """

        res_1 = self.client.post('/api/v1/register', json=self.user)
        data_1 = res_1.get_json()

        self.assertEqual(res_1.status_code, 201)
        self.assertEqual(data_1['status'], 201)

        self.user.update({
            'firstname' : 'Jane',
            'lastname' : 'Dreary',
            'username' : 'jdreary'
        })

        res_2 = self.client.post('/api/v1/register', json=self.user)
        data_2 = res_2.get_json()

        self.assertEqual(res_2.status_code, 409)
        self.assertEqual(data_2['status'], 409)
        self.assertEqual(data_2['message'], 'Email already exists')

    def test_signup_existing_username(self):
        """ Test sign up with existing username """

        res_1 = self.client.post('/api/v1/register', json=self.user)
        data_1 = res_1.get_json()

        self.assertEqual(res_1.status_code, 201)
        self.assertEqual(data_1['status'], 201)

        self.user.update({
            'firstname' : 'Jane',
            'lastname' : 'Dreary',
            'email' : 'jdreary@gmail.com'
        })

        res_2 = self.client.post('/api/v1/register', json=self.user)
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

        self.super_user.clear()

        res = self.client.post('/api/v1/login', json=self.super_user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_login_unregistered_user(self):
        """ Test login with unregistered user credentials """

        res = self.client.post('/api/v1/login', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'User not found')

    def test_login(self):
        """ Test successfull login """

        res = self.client.post('/api/v1/login', json=self.super_user)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'User logged in successfully')

    def test_login_no_username_provided(self):
        """ Test login with no username provided """

        self.super_user.pop('username', None)

        res = self.client.post('/api/v1/login', json=self.super_user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid credentials')

    def test_login_invalid_password(self):
        """ Test login with invalid password """

        self.super_user.update({'password': 'asfdgfdngf'})

        res = self.client.post('/api/v1/login', json=self.super_user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data. Please fill all required fields')

    def test_refresh_access_token_no_token_passed(self):
        """ Test refresh access token without passing refresh token"""

        res = self.client.post('/api/v1/refresh-token')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['msg'], 'Missing Authorization Header')

    def test_refresh_access_token_passing_access_token(self):
        """ Test refresh access token passing access token """

        res = self.client.post('/api/v1/refresh-token', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['msg'], 'Only refresh tokens are allowed')


    def test_refresh_access_token(self):
        """ Test refresh access token successfully"""

        self.headers.update({'Authorization': 'Bearer {}'.format(self.refresh_token)})

        res = self.client.post('/api/v1/refresh-token', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Token refreshed successfully')

    def test_logout_no_access_token(self):
        """ Test logout without access token """

        res = self.client.post('/api/v1/logout')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['msg'], 'Missing Authorization Header')

    def test_logout_passing_refesh_token(self):
        """ Test logout passing refresh token """

        self.headers.update({'Authorization': 'Bearer {}'.format(self.refresh_token)})

        res = self.client.post('/api/v1/logout', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['msg'], 'Only access tokens are allowed')

    def test_logout(self):
        """ Test logout successfully """

        res = self.client.post('/api/v1/logout', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Logged out successfully')

    def test_logout_revoked_token(self):
        """ Test logout without access token """

        self.client.post('/api/v1/logout', headers=self.headers)

        res = self.client.post('/api/v1/logout', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['msg'], 'Token has been revoked')


    