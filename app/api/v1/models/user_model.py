from datetime import datetime
from werkzeug.security import generate_password_hash
from ..utils.utils import generate_id

users = []

class User(object):
    """ Model class for the user object """

    def save(self, data):
        """ Function to save new user """
        data['id'] = generate_id(users)
        data['password'] = generate_password_hash(data['password'])
        data['registered_on'] = datetime.now()
        data['modified_on'] = datetime.now()
        data['is_admin'] = False
        users.append(data)
        return data
        
    def exists(self, key, value):
        """ Function to check if user with provided value exists for provided key """
        found_users = [user for user in users if value == user[key]]
        return len(found_users) > 0 
