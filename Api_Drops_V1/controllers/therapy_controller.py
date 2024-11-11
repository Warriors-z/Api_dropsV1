from flask import abort, jsonify, request
from ..schemas.therapy_schema import TherapyInsertSchema, ValidationError
from ..models.dtos.therapy_dto import Therapy
from ..models.therapy import (
    get_all_therapies, 
    create_therapy, 
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

def insert_therapy():
    data = request.get_json()
    print(data)
    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    try:
        validated_user_therapy = TherapyInsertSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400


    stretcher_number = validated_user_therapy['stretcher_number']
    balance_id = validated_user_therapy['balance_id']
    patient_id = validated_user_therapy['patient_id']
    nurse_id = validated_user_therapy['nurse_id']
    user_id = validated_user_therapy['user_id']


    if not all([stretcher_number, balance_id, patient_id, nurse_id, user_id]):
        abort(400, description="Error: Faltan datos necesarios para la creacion de la terapia.")

    newTherapy = Therapy(stretcher_number, balance_id, patient_id, nurse_id, user_id)
    
    

    if not create_therapy(newTherapy):
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