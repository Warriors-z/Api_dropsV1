from marshmallow import Schema, fields, validate, ValidationError

class PatientInsertSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=70))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=70))
    second_last_name = fields.Str(required=False, validate=validate.Length(min=2, max=70))
    birth_date = fields.Str(required=True)
    genre = fields.Str(required=True, validate=validate.Length(min=1, max=15))
    ci = fields.Str(required=True, validate=validate.Length(max=12))
    user_id = fields.Int(required=True)

class PatientUpdateSchema(Schema):
    patient_id = fields.Int(required=True) 
    name = fields.Str(required=True, validate=validate.Length(min=2, max=70))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=70))
    second_last_name = fields.Str(required=False, validate=validate.Length(min=2, max=70))
    birth_date = fields.Str(required=True)
    genre = fields.Str(required=True, validate=validate.Length(min=1, max=15))
    ci = fields.Str(required=True, validate=validate.Length(max=12))
    user_id = fields.Int(required=True)

class PatientDeleteSchema(Schema):
    patient_id = fields.Int(required=True)
    user_id = fields.Int(required=True)