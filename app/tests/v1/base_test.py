import unittest
from app import create_app

class BaseTest(unittest.TestCase):
    """ Base class for Tests """

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def tearDown(self):
        self.app = None
