from marshmallow import Schema, fields, validate,ValidationError

class UserInsertSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=70))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=70))
    second_last_name = fields.Str(required=False, validate=validate.Length(min=2, max=70))
    phone = fields.Str(required=False, validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True, validate=validate.Length(max=45))
    address = fields.Str(required=True, validate=validate.Length(min=10))
    birth_date = fields.Str(required=True)
    genre = fields.Str(required=True, validate=validate.Length(min=1, max=15))
    ci = fields.Str(required=True, validate=validate.Length(max=12))
    role_id = fields.Int(required=True)

class UserUpdateSchema(Schema):
    user_id = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=70))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=70))
    second_last_name = fields.Str(required=False, validate=validate.Length(min=2, max=70))
    phone = fields.Str(required=False, validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True, validate=validate.Length(max=45))
    address = fields.Str(required=True, validate=validate.Length(min=10))
    birth_date = fields.Str(required=True)
    genre = fields.Str(required=True, validate=validate.Length(min=1, max=15))
    ci = fields.Str(required=True, validate=validate.Length(max=12))
    role_id = fields.Int(required=True)