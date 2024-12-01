from flask import Blueprint
from ..controllers.token_controller import token_required, role_required
from ..controllers.therapy_controller import (
    list_therapies, 
    insert_therapy, 
    list_balances, list_nurses, list_patients,
    info_therapy,
    list_therapies_nurses,
    list_therapies_asign
)

therapy_bp = Blueprint('therapy',__name__, url_prefix='/api/v1')

@therapy_bp.route('/therapies', methods=['GET'])
@token_required
@role_required([1,2,4])
def get_therapies():
    """
    Obtener lista de terapias
    ---
    tags:
      - Terapias
    responses:
      200:
        description: Lista de terapias
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """

    return list_therapies()

@therapy_bp.route('/therapy/create',methods=['POST'])
@token_required
@role_required([1,2,4])
def create_therapy():
    """
    Crear una nueva Therapia
    ---
    tags:
      - Terapias
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CreateTherapy
          required:
            - stretcher_number
            - balance_id
            - patient_id
            - nurse_id
            - user_id
          properties:
            stretcher_number:
              type: string
              description: Numero de la camilla
            balance_id:
              type: integer
              description: ID de la balanza
            patient_id:
              type: integer
              description: ID del paciente
            nurse_id:
              type: integer
              description: ID del enfermero
            user_id:
              type: integer
              description: ID del usuario creador
    responses:
      201:
        description: Therapia creado exitosamente
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      400:
        description: Error en los datos enviados
    """
    return insert_therapy()

@therapy_bp.route('/therapy/patients', methods=['GET'])
@token_required
@role_required([1,2,4])
def get_patients():
    """
    Obtener lista de pacientes
    ---
    tags:
      - Terapias
    responses:
      200:
        description: Lista de pacientes
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """
    return list_patients()

@therapy_bp.route('/therapy/nurses',methods=['GET'])
@token_required
@role_required([1,2,4])
def get_nurses():
    """
    Obtener lista de enfermeros
    ---
    tags:
      - Terapias
    responses:
      200:
        description: Lista de enfermeros
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """
    return list_nurses()

@therapy_bp.route('/therapy/balances',methods=['GET'])
@token_required
@role_required([1,2,4])
def get_balances():
    """
    Obtener lista de balanzas
    ---
    tags:
      - Terapias
    responses:
      200:
        description: Lista de balanzas
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """
    return list_balances()

@therapy_bp.route('/therapy/info/<int:therapy_id>',methods=['GET'])
@token_required
@role_required([1,2,4])
def get_therapy_info_by_id(therapy_id):
    """
    Obtener informacion de la therapia por ID
    ---
    tags:
      - Terapias
    parameters:
      - name: therapy_id
        in: path
        type: integer
        required: true
        description: ID de la terapia
    responses:
      200:
        description: Datos de la terapia
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """
    return info_therapy(therapy_id)

@therapy_bp.route('/therapies/nurses/<int:nurse_id>', methods=['GET'])
@token_required
@role_required([2,4])
def get_therapies_nurse_by_id(nurse_id):
    """
    Obtener therapias asignadas al enfermero por su ID
    ---
    tags:
      - Terapias
    parameters:
      - name: nurse_id
        in: path
        type: integer
        required: true
        description: ID del enfermero
    responses:
      200:
        description: Datos de las terapias
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """
    return list_therapies_nurses(nurse_id)

@therapy_bp.route('/therapies/asign', methods=['GET'])
# @token_required
# @role_required([4])
def get_therapies_assignment():
    """
    Obtener lista de todas las terapias asignadas
    ---
    tags:
      - Terapias
    responses:
      200:
        description: Lista de terapias asignadas
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """
    return list_therapies_asign()