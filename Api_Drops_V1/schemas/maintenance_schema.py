from marshmallow import Schema, fields, validate, ValidationError

class MaintenanceInsertSchema(Schema):
    last_factor = fields.Decimal(required=True, places=2)
    user_id = fields.Int(required=True)
    balance_id = fields.Int(required=True)

class MaintenanceUpdateSchema():
    balance_code = fields.Str(required=True)
    