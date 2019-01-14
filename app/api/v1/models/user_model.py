from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.utils import generate_id
from .base_model import Model

users = []

class User(Model):
    """ Model class for the User object """

    def __init__(self):
        super().__init__(users)

    def save(self, data):
        """ Function to save new user """

        data['id'] = generate_id(self.collection)
        data['password'] = generate_password_hash(data['password'])
        data['is_admin'] = False
        return super().save(data)

    @staticmethod
    def checkpassword(hashed_password, password):
        """ Function to check if passwords match """
        
        return check_password_hash(hashed_password, password)
