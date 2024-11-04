from marshmallow import Schema, fields,validate, ValidationError

class TherapyInsertSchema(Schema):
    stretcher_number = fields.Str(required=True, validate=validate.Length(max=30))
    patient_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    nurse_id = fields.Int(required=True)
    balance_id = fields.Int(required=True) 