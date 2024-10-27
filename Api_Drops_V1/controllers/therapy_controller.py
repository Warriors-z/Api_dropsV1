from flask import abort, jsonify, request
from ..models.therapy import (
    get_all_therapies, 
    get_therapy_by_id, 
    create_therapy, 
    update_therapy, 
    delete_therapy, 
    get_all_nurses, 
    get_all_patients, 
    get_all_balances,
    get_info_therapy
)

def list_therapies():
    therapies = get_all_therapies()
    if therapies is None:
        abort(404, description = "Error: Registros no encontrados.")
    return jsonify(therapies)

def therapy_by_id(therapy_id):
    therapy = get_therapy_by_id(therapy_id)
    if therapy is None:
        abort(404, description="Error: Registro no encontrado.")
    return jsonify(therapy)

def insert_therapy():
    data = request.get_json()
    
    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    stretcher_number = data.get('stretcher_number')
    id_balance = data.get('id_balance')
    id_patient = data.get('id_patient')
    id_nurse = data.get('id_nurse')
    id_user = data.get('id_user')

    if not all([stretcher_number, id_balance, id_patient, id_nurse, id_user]):
        abort(400, description="Error: Faltan datos necesarios para la creacion de la terapia.")

    therapy = create_therapy(stretcher_number, id_balance, id_patient, id_nurse, id_user)

    if not therapy:
        abort(500, description="Error interno del servidor durante la creacion de la terapia!")
    return jsonify({
        "message": "Creacion de Terapia Exitosa!",
    }), 201

def list_nurses():
    nurses = get_all_nurses()
    if nurses is None:
        abort(404, description="Error: Registros no encontrados.")
    return jsonify(nurses)

def list_balances():
    balances = get_all_balances()
    if balances is None:
        abort(404, description="Error: Registros no encontrados.")
    return jsonify(balances)

def list_patients():
    patients = get_all_patients()
    if patients is None:
        abort(404, description="Error: Registros no encontrados.")
    return jsonify(patients)

def info_therapy(therapy_id):
    therapy = get_info_therapy(therapy_id)
    if therapy is None:
        abort(404, description="Error: Informacion no encontrada.")
    return jsonify(therapy)