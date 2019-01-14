
def generate_id(collection):
    """ Function to generate ID for collection """

    if len(collection) == 0:
        return 1
    else:
        return collection[-1]['id']+1