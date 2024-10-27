from flask import abort, jsonify, request
from ..models.balance import (
    get_all_balances,
    get_balance_by_id,
    create_balance,
    update_balance,
    delete_balance
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

def insert_balance():
    data = request.get_json()

    if not data:
        abort(400, description="Error: Nose proporcionaron datos.")

    balance_code = data.get('balance_code')
    #actually_factor = data.get('actually_factor')
    user_id = data.get('user_id')

    if not all([balance_code, user_id]):
        abort(400, description="Error: Faltan datos necesarios para la creacion de la Balanza.")
    
    balance = create_balance(balance_code, user_id)

    if not balance:
        abort(500, description="Error: Fallo interno del servidor durante la creacion de la Balanza.")
    return jsonify({
        "message": "Creacion de Balanza Exitosa!"
    }), 201

def edit_balance():
    data = request.get_json()

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    balance_id = data.get('balance_id') 
    balance_code = data.get('balance_code')
    user_id = data.get('user_id')

    if not all([balance_id, balance_code, user_id]):
        abort(400, description="Error: Faltan datos necesarios para la actualización de la Balanza.")

    balance_updated = update_balance(balance_id, balance_code, user_id)

    if not balance_updated:
        abort(500, description="Error interno del servidor durante la actualización de la Balanza.")

    return jsonify({
        "message": "Actualización de Balanza Exitosa!"
    }), 200

def remove_balance():
    data = request.get_json()

    if not data:
        abort(400, description="Error: Nose proporcionaron datos.")

    balance_id = data.get('balance_id')
    user_id = data.get('user_id')

    if not all([balance_id, user_id]):
        abort(400, description="Error: Faltan datos necesarios para la Eliminacion de la Balanza.")

    balance_deleted  = delete_balance(balance_id, user_id)

    if not balance_deleted:
        abort(400, description="Error: Fallo en la eliminacion de la Balanza!")
    return jsonify({
        "message": "Eliminacion de Balanza Exitosa!"
    }), 200