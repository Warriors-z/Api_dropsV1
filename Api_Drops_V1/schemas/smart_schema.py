from marshmallow import Schema, fields, validate, ValidationError

class SmartInsertSchema(Schema):
    code_rfid = fields.Str(required=True, validate=validate.Length(max=10))
    user_id = fields.Int(required=False)

class SmartUpdateSchema(Schema):
    smart_id = fields.Int(requires=True)
    code_rfid = fields.Str(required=True, validate=validate.Length(max=10))
    available = fields.Int(required=True)
    user_id = fields.Int(required=False)

class SmartAssignmentSchema(Schema):
    smart_id = fields.Int(requires=True)
    user_id = fields.Int(required=True)
