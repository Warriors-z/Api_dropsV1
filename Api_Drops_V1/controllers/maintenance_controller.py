from flask import abort, jsonify, request
from ..schemas.maintenance_schema import MaintenanceInsertSchema, MaintenanceUpdateSchema, ValidationError
from ..models.dtos.maintenance_dto import Maintenance
from ..models.maintenance import (
    create_maintenance,
    get_balance_to_maintenance_by_code,
)

def insert_maintenance():
    data = request.get_json()
    if not data:
        abort(400, description="Error: Nose proporcionaron datos.")

    try:
        validated_maintenance_data = MaintenanceInsertSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    

    balance_id = validated_maintenance_data['balance_id']
    user_id = validated_maintenance_data['user_id']
    last_factor = validated_maintenance_data['last_factor']
    print(last_factor)

    if not all([balance_id, user_id, last_factor]):
        abort(400, description="Error: Faltan datos necesarios para el registro del Mantenimiento.")

    maintenance = Maintenance(None,balance_id, user_id, last_factor, None)
    print(maintenance.last_factor)
    if not create_maintenance(maintenance):
        abort(500, description="Error: Fallo interno del servidor durante el registro del Mantenimiento.")
    return jsonify({
        "message": "Registro exitoso!"
    }), 201

def maintenance_balance_by_code(balance_code):
    maintenance = get_balance_to_maintenance_by_code(balance_code)
    print(maintenance)
    if maintenance is None:
        abort(404, description = "Error: Registro no encontrado.")
    return jsonify(maintenance)