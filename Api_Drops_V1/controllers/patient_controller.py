from flask import abort, jsonify, request
from ..models.patient import (
    get_all_patients,
    get_patient_by_id,
    create_patient,
    update_patient,
    delete_patient
)

def list_patients():
    patients = get_all_patients()
    if patients is None:
        abort(404, description="Error: Registros no encontrados.")
    return jsonify(patients)

def patient_by_id(patient_id):
    patient = get_patient_by_id(patient_id)
    if patient is None:
        abort(404, description="Error: Registro no encontrado.")
    return jsonify(patient)

def inser_patient():
    data = request.get_json()

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    name = data.get('name')
    last_name = data.get('last_name')
    second_last_name = data.get('second_last_name')
    birth_date = data.get('birth_date')
    ci = data.get('ci')
    user_id = data.get('user_id')

    if not all([name, last_name, birth_date, ci, user_id]):
        abort(400,description="Error: Faltan datos necesarios para la creacion del Paciente.")

    patient = create_patient(name, last_name, second_last_name, birth_date, ci, user_id)

    if not patient:
        abort(500, description="Error: Fallo interno del servidor durante la creacion del paciente.")
    return jsonify({
        "message": "Creacion de Paciente Exitoso!"
    }), 201

def edit_patient():
    data = request.get_json()

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    patient_id = data.get('patient_id')
    name = data.get('name')
    last_name = data.get('last_name')
    second_last_name = data.get('second_last_name')
    birth_date = data.get('birth_date')
    ci = data.get('ci')
    user_id = data.get('user_id')

    if not all([patient_id, name, last_name, birth_date, ci, user_id]):
        abort(400,description="Error: Faltan datos necesarios para la edicion del Paciente.")

    patient = update_patient(patient_id, name, last_name, second_last_name, birth_date, ci, user_id)

    if not patient:
        abort(500, description="Error: Fallo interno del servidor durante la actualizacion del paciente.")
    return jsonify({
        "message": "Edicion de Paciente Exitoso!"
    }), 200

def remove_patient():
    data = request.get_json()

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    patient_id = data.get('patient_id')
    user_id = data.get('user_id')

    if not all([patient_id, user_id]):
        abort(400,description="Error: Faltan datos necesarios para la eliminacion del Paciente.")

    patient = delete_patient(patient_id, user_id)

    if not patient:
        abort(500, description="Error: Fallo interno del servidor durante la eliminacion del paciente.")
    return jsonify({
        "message": "Eliminacion de Paciente Exitoso!"
    }), 200