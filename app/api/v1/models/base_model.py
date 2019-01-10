from datetime import datetime
from ..utils.utils import generate_id

class Model(object):
    """ Base Model class for objects """

    def __init__(self, collection):
        """ Initializes list of object type """
        self.collection = collection

    def save(self, data):
        """ Function to save object """
        data['created_on'] = datetime.now()
        data['modified_on'] = datetime.now()
        self.collection.append(data)
        return data

    def exists(self, key, value):
        """ Function to check if object exists with key, value pair """
        items = [item for item in self.collection if item[key] == value]
        return len(items) > 0

    def find(self, key, value):
        """ Function to find item by key, value par """
        items = [item for item in self.collection if item[key] == value]
        return items[0]

    def all(self):
        """ Function to fetch all items """
        return self.collection
        