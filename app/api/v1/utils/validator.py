import re
from marshmallow import ValidationError

def required(value):
    """Validate that field under validation does not contain null value."""

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
    if not re.match(r'[A-Za-z0-9@#$%^&+=]{6,}', password):
        raise ValidationError('Weak password provided')
        