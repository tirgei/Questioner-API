from marshmallow import Schema, fields
from ..utils.validator import required

class QuestionSchema(Schema):
    """ Class to validate schema for Question object """

    id = fields.Int(dump_only=True)
    title = fields.Str(required=False, validate=(required))
    body = fields.Str(required=True, validate=(required))
    meetup_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)
    votes = fields.Int(dump_only=True)
    created_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)