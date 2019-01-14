import re
from marshmallow import ValidationError

def required(value):
    """Validate that field under validation does not contain null value"""

    if isinstance(value, str):
        if not value.strip(' '):
            raise ValidationError('This parameter cannot be null')
        return value
    elif value:
        return value

def email(value):
    """ Validate email format """

    if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)", value):
        raise ValidationError('Invalid email format')

    return value

def password(password):
    """ Validate password is Strong """
    
    message = 'Invalid password'

    if len(password) < 8:
        raise ValidationError(message)

    scores = {}

    for letter in password:
        if letter.islower():
            scores['has_lower'] = 1

        if letter.isupper():
            scores['has_upper'] = 1

        if letter.isdigit():
            scores['has_digit'] = 1

    if sum(scores.values()) < 3:
        raise ValidationError(message)