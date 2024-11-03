from flask import abort, jsonify, request
from ..schemas.patient_schema import PatientInsertSchema, PatientUpdateSchema, PatientDeleteSchema, ValidationError
from ..models.dtos.patient_dto import Patient
from ..models.patient import (
    get_all_patients,
    get_patient_by_id,
    create_patient,
    update_patient,
    delete_patient,
    check_exists_patient
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

    try:
        validated_patient_data = PatientInsertSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    name = validated_patient_data['name']
    last_name = validated_patient_data['last_name']
    second_last_name = validated_patient_data['second_last_name']
    birth_date = validated_patient_data['birth_date']
    genre = validated_patient_data['genre']
    ci = validated_patient_data['ci']
    user_id = validated_patient_data['user_id']

    if not all([name, last_name, birth_date, ci, user_id]):
        abort(400,description="Error: Faltan datos necesarios para la creacion del Paciente.")

    patient = Patient(name, last_name, second_last_name, birth_date, genre, ci, user_id)

    patient_ci_exists = check_exists_patient(ci)

    if patient_ci_exists is not None:
        abort(400, description="El paciente ya esta registrado.")

    if not create_patient(patient):
        abort(500, description="Error: Fallo interno del servidor durante la creacion del paciente.")
    return jsonify({
        "message": "Creacion de Paciente Exitoso!"
    }), 201

def edit_patient():
    data = request.get_json()

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    try:
        validated_patient_data = PatientUpdateSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    patient_id = validated_patient_data['patient_id']
    name = validated_patient_data['name']
    last_name = validated_patient_data['last_name']
    second_last_name = validated_patient_data['second_last_name']
    birth_date = validated_patient_data['birth_date']
    genre = validated_patient_data['genre']
    ci = validated_patient_data['ci']
    user_id = validated_patient_data['user_id']

    if not all([patient_id, name, last_name, birth_date, ci, user_id]):
        abort(400,description="Error: Faltan datos necesarios para la edicion del Paciente.")

    patient = Patient(name, last_name, second_last_name, birth_date, genre,ci, user_id, patient_id)

    if not update_patient(patient):
        abort(500, description="Error: Fallo interno del servidor durante la actualizacion del paciente.")
    return jsonify({
        "message": "Edicion de Paciente Exitoso!"
    }), 200

def remove_patient():
    data = request.get_json()

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    try:
        validated_patient_data = PatientDeleteSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    patient_id = validated_patient_data['patient_id']
    user_id = validated_patient_data['user_id']

    if not all([patient_id, user_id]):
        abort(400,description="Error: Faltan datos necesarios para la eliminacion del Paciente.")

    if not delete_patient(patient_id, user_id):
        abort(500, description="Error: Fallo interno del servidor durante la eliminacion del paciente.")
    return jsonify({
        "message": "Eliminacion de Paciente Exitoso!"
    }), 200