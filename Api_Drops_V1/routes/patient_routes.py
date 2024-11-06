from flask import Blueprint
from ..controllers.token_controller import token_required, role_required
from ..controllers.patient_controller import (
    list_patients,
    patient_by_id,
    inser_patient,
    edit_patient,
    remove_patient
)

patient_bp = Blueprint('patient',__name__, url_prefix='/api/v1')

@patient_bp.route('/patients', methods=['GET'])
#@token_required
#@role_required([1, 2])
def get_patients():
    """
    Obtener lista de pacientes
    ---
    tags:
      - Pacientes  
    responses:
      200:
        description: Lista de pacientes
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Lista de pacientes no encontrada.  
    """
    return list_patients()

@patient_bp.route('/patient/byId/<int:patient_id>', methods=['GET'])
#@token_required
#@role_required([1, 2])
def get_patient_by_id(patient_id):
    """
    Obtener paciente por ID
    ---
    tags:
      - Pacientes
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: ID del paciente  
    responses:
      200:
        description: Datos del paciente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Paciente no encontrada  
    """
    return patient_by_id(patient_id)

@patient_bp.route('/patient/create', methods=['POST'])
#@token_required
#@role_required([1,2])
def create_patient():
    """
    Crear un nuevo paciente
    ---
    tags:
      - Pacientes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CreatePatient
          required:
            - name
            - last_name
            - second_last_name
            - birth_date
            - genre
            - ci
            - user_id
          properties:
            name:
              type: string
              description: Nombre del paciente
            last_name:
              type: string
              description: Apellido Paterno del paciente
            second_last_name:
              type: string
              description: Apellido Materno del paciente
            birth_date:
              type: string
              description: Fecha de nacimiento del paciente
            genre:
              type: string
              description: Genero del paciente
            ci:
              type: string
              description: Carnet de identidad del paciente
            user_id:
              type: integer
              description: ID del usuario creador
    responses:
      201:
        description: Paciente creado exitosamente
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      400:
        description: Error en los datos enviados
    """
    return inser_patient()

@patient_bp.route('/patient/update', methods=['PUT'])
#@token_required
#@role_required([1,2])
def modify_patient():
    """
    Actualizar un paciente existente
    ---
    tags:
      - Pacientes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UpdatePatient
          required:
            - patient_id
            - name
            - last_name
            - second_last_name
            - birth_date
            - genre
            - ci
            - user_id
          properties:
            patient_id:
                type: integer
                description: ID del paciente a modificar
            name:
              type: string
              description: Nombre del paciente
            last_name:
              type: string
              description: Apellido Paterno del paciente
            second_last_name:
              type: string
              description: Apellido Materno del paciente
            birth_date:
              type: string
              description: Fecha de nacimiento del paciente
            genre:
              type: string
              description: Genero del paciente
            ci:
              type: string
              description: Carnet de identidad del paciente
            user_id:
              type: integer
              description: ID del usuario modificador
    responses:
      201:
        description: Paciente actualizado exitosamente
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      400:
        description: Error en los datos enviados
    """
    return edit_patient()

@patient_bp.route('/patient/delete', methods=['DELETE'])
#@token_required
#@role_required([1,2])
def delete_patient():
    """
    Eliminar una paciente existente
    ---
    tags:
      - Pacientes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: DeletePatient
          required:
            - patient_id
            - user_id
          properties:
            patient_id:
              type: integer
              description: ID del paciente a eliminar
            user_id:
              type: integer
              description: ID del usuario eliminador 
    responses:
      200:
        description: Paciente eliminado exitosamente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Paciente no encontrado 
    """
    return remove_patient()