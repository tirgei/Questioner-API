from marshmallow import Schema, fields, post_dump
from ..utils.validator import email, password, required
from ..models.user_model import User

class UserSchema(Schema):
    """ Class to validate schema for User object """

    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    othername = fields.Str(required=False)
    username = fields.Str(required=True, validate=(required))
    phone_number = fields.Str(required=True, validate=(required))
    email = fields.Email(required=True, validate=(email))
    password = fields.Str(required=True, validate=(password))
    registered_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)
    is_admin = fields.Bool(dump_only=True)

