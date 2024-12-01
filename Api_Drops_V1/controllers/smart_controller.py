from flask import abort, jsonify, request
from ..schemas.smart_schema import SmartInsertSchema, SmartUpdateSchema, SmartAssignmentSchema,ValidationError
from ..models.dtos.smart_dto import Smart
from ..models.smart import (
    get_all_smarts,
    get_smart_by_id,
    create_smart,
    update_smart,
    delete_smart,
    check_exists_smart,
    assignment_smart,
    get_nurses_whithout_smart
)

def list_smarts():
    smarts = get_all_smarts()
    if smarts is None:
        abort(404, description = "Error: Registros no encontrados.")
    return jsonify(smarts)

def list_nurses_without_smarts():
    nurses = get_nurses_whithout_smart()
    if nurses is None:
        abort(404, description="Error: Registros no encontrados.")
    return jsonify(nurses)

def smart_by_id(smart_id):
    smart = get_smart_by_id(smart_id)
    if smart is None:
        abort(404, description="Error: Registro no encontrado.")
    return jsonify(smart)

def verify_exist_smart_code(code):
    exist_smart = check_exists_smart(code)
    if exist_smart is not None:
        return jsonify({'code_rfid': exist_smart})
    return jsonify({'code_rfid': exist_smart})

def insert_smart():
    data = request.get_json()

    if not data:
        abort(400, description="Error: Nose proporcionaron datos.")

    try:
        validated_smart_data = SmartInsertSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    code_rfid = validated_smart_data['code_rfid']

    if not code_rfid:
        abort(400, description="Error: Faltan datos necesarios para la creacion de la Manilla.")
    
    smart = Smart(code_rfid)

    code_rfid_exists = check_exists_smart(code_rfid)

    if code_rfid_exists is not None:
        abort(400, description="La manilla ya esta registrada.")

    if not create_smart(smart):
        abort(500, description="Error: Fallo interno del servidor durante la creacion de la Manilla.")
    return jsonify({
        "message": "Creacion de Manilla Exitosa!"
    }), 201

def asign_smart():
    data = request.get_json()
    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    print(jsonify(data))

    try:
        validated_smart_data = SmartAssignmentSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = validated_smart_data['user_id']
    smart_id = validated_smart_data['smart_id']

    if not all([user_id, smart_id]):
        abort(400, description="Error: Faltan datos necesarios para la asignacion de la Manilla.")

    assigned_smart = Smart(None, None, smart_id, user_id) 

    if not assignment_smart(assigned_smart):
        abort(500, description="Error interno del servidor durante la asignacion de la Manilla.")

    return jsonify({
        "message": "Asignacion de Manilla Exitosa!"
    }), 200

def edit_smart():
    data = request.get_json()

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    try:
        validated_smart_data = SmartUpdateSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    smart_id = validated_smart_data['smart_id'] 
    code_rfid = validated_smart_data['code_rfid']
    available = validated_smart_data['available']
    user_id = validated_smart_data['user_id']

    if not all([smart_id, code_rfid]):
        abort(400, description="Error: Faltan datos necesarios para la actualización de la Manilla.")


    if (user_id == 0):
        user_id = None

    smart_updated = Smart(code_rfid, available,smart_id,user_id)

    if not update_smart(smart_updated):
        abort(500, description="Error interno del servidor durante la actualización de la Manilla.")

    return jsonify({
        "message": "Actualización de Manilla Exitosa!"
    }), 200

def remove_smart(smart_id):
    if smart_id is None:
        abort(400, description="Error: Falta el ID de la manilla a eliminar.")

    if not delete_smart(smart_id):
        abort(500, description="Error: Fallo en la eliminacion de la Manilla!")
    return jsonify({
        "message": "Eliminacion de Manilla Exitosa!"
    }), 200