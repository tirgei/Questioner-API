from marshmallow import Schema, fields, post_dump
from ..utils.validator import required

class CommentSchema(Schema):
    """ Class to validate schema for Comment object """

    id = fields.Int(dump_only=True)
    body = fields.Str(required=True, validate=(required))
    user = fields.Int(required=False)