from flask import abort, jsonify, request
from ..schemas.balance_schema import BalanceInsertSchema, BalanceUpdateSchema,BalanceDeleteSchema,ValidationError
from ..models.dtos.balance_dto import Balance
from ..models.balance import (
    get_all_balances,
    get_balance_by_id,
    create_balance,
    update_balance,
    delete_balance,
    check_exists_balance
)

def list_balances():
    balances = get_all_balances()
    if balances is None:
        abort(404, description="Error: Registros no encontrados.")
    return jsonify(balances)

def balance_by_id(balance_id):
    balance = get_balance_by_id(balance_id)
    if balance is None:
        abort(404, description="Error: Registro no encontrado.")
    return jsonify(balance)

def verify_exist_balance_code(code):
    exist_code = check_exists_balance(code)
    if exist_code is not None:
        return jsonify({'balance_code':exist_code})
    return jsonify({'balance_code':exist_code})

def insert_balance():
    data = request.get_json()

    if not data:
        abort(400, description="Error: Nose proporcionaron datos.")

    try:
        validated_balance_data = BalanceInsertSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    balance_code = validated_balance_data['balance_code']
    user_id = validated_balance_data['user_id']

    if not all([balance_code, user_id]):
        abort(400, description="Error: Faltan datos necesarios para la creacion de la Balanza.")
    
    balance = Balance(balance_code)

    balance_code_exists = check_exists_balance(balance_code)

    if balance_code_exists is not None:
        abort(400, description="La balanza ya esta registrada.")

    if not create_balance(balance):
        abort(500, description="Error: Fallo interno del servidor durante la creacion de la Balanza.")
    return jsonify({
        "message": "Creacion de Balanza Exitosa!"
    }), 201

def edit_balance():
    data = request.get_json()

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    try:
        validated_balance_data = BalanceUpdateSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    balance_id = validated_balance_data['balance_id'] 
    balance_code = validated_balance_data['balance_code']
    user_id = validated_balance_data['user_id']

    if not all([balance_id, balance_code, user_id]):
        abort(400, description="Error: Faltan datos necesarios para la actualización de la Balanza.")



    balance_updated = Balance(balance_code, user_id, None,balance_id)

    if not update_balance(balance_updated):
        abort(500, description="Error interno del servidor durante la actualización de la Balanza.")

    return jsonify({
        "message": "Actualización de Balanza Exitosa!"
    }), 200

def remove_balance():
    data = request.get_json()

    if not data:
        abort(400, description="Error: Nose proporcionaron datos.")

    try:
        validated_balance_data = BalanceDeleteSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    balance_id = validated_balance_data['balance_id'] 
    user_id = validated_balance_data['user_id']

    if not all([balance_id, user_id]):
        abort(400, description="Error: Faltan datos necesarios para la Eliminacion de la Balanza.")

    balance_deleted = Balance(None,user_id,None, balance_id)

    if not delete_balance(balance_deleted):
        abort(400, description="Error: Fallo en la eliminacion de la Balanza!")
    return jsonify({
        "message": "Eliminacion de Balanza Exitosa!"
    }), 200