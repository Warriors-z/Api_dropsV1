from marshmallow import Schema, fields, ValidationError

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role_id = fields.Int(required=True)