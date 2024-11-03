from marshmallow import Schema, fields, validate, ValidationError

class BalanceInsertSchema(Schema):
    balance_code = fields.Str(required=True, validate=validate.Length(max=25))
    user_id = fields.Int(requires=True)

class BalanceUpdateSchema(Schema):
    balance_id = fields.Int(required=True)
    balance_code = fields.Str(required=True, validate=validate.Length(max=25))
    user_id = fields.Int(requires=True)

class BalanceDeleteSchema(Schema):
    balance_id = fields.Int(required=True)
    user_id = fields.Int(requires=True)