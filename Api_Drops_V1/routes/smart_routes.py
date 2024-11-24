from flask import Blueprint
from ..controllers.token_controller import token_required, role_required
from ..controllers.smart_controller import(
    list_smarts,
    smart_by_id,
    insert_smart,
    edit_smart,
    remove_smart,
    asign_smart,
    list_nurses_without_smarts,
    verify_exist_smart_code
)

smart_bp = Blueprint('smart',__name__, url_prefix='/api/v1')

@smart_bp.route('/smarts', methods=['GET'])
@token_required
@role_required([1])
def get_smarts():
    """
    Obtener lista de Manillas
    ---
    tags:
      - Manillas  
    responses:
      200:
        description: Lista de manillas
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Lista de manillas no encontrada.  
    """
    return list_smarts()

@smart_bp.route('/nurses/whithout/smarts', methods=['GET'])
@token_required
@role_required([1])
def get_all_nurses_whithout_smarts():
    """
    Obtener lista de Enfermeros sin manillas asignadas
    ---
    tags:
      - Manillas  
    responses:
      200:
        description: Lista de enfermeros sin manillas
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Lista de enfermeros sin manillas no encontrada.  
    """
    return list_nurses_without_smarts()


@smart_bp.route('/smart/byId/<int:smart_id>', methods=['GET'])
@token_required
@role_required([1])
def get_smart_by_id(smart_id):
    """
    Obtener manilla por ID
    ---
    tags:
      - Manillas
    parameters:
      - name: smart_id
        in: path
        type: integer
        required: true
        description: ID de la manilla  
    responses:
      200:
        description: Datos de la manilla
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Manilla no encontrada  
    """
    return smart_by_id(smart_id)

@smart_bp.route('/smart/checkExist/<string:smart_code>', methods=['GET'])
@token_required
@role_required([1])
def verify_exist_smart(smart_code):
    """
    Verificar si existe la manilla
    ---
    tags:
      - Manillas
    parameters:
      - name: smart_code
        in: path
        type: string
        required: true
        description: CODIGO de la manilla
    responses:
      200:
        description: Datos de la manilla
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      500:
        description: Error interno del servidor
      400:
        description: Fallo en verificacion de la manilla
    """
    return verify_exist_smart_code(smart_code)


@smart_bp.route('/smart/create', methods=['POST'])
@token_required
@role_required([1])
def create_smart():
    """
    Crear nueva manilla
    ---
    tags:
      - Manillas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CreateSmart
          required:
            - code_rfid
          properties:
            code_rfid:
              type: string
              description: Codigo RFID de la manilla
    responses:
      200:
        description: Manilla creada correctamente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente  
    """
    return insert_smart()

@smart_bp.route('/smart/update', methods=['PUT'])
@token_required
@role_required([1])
def modify_smart():
    """
    Actualizar una manilla existente
    ---
    tags:
      - Manillas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UpdateSmart
          required:
            - code_rfid
            - available
            - user_id
            - smart_id
          properties:
            code_rfid:
              type: string
              description: Codigo de la manilla
            available:
              type: integer
              description: Estado de la manilla (1 disponible, 0 No disponible)
            user_id:
              type: integer
              description: ID del usuario asignado
            smart_id:
              type: integer
              description: ID de la manilla  
    responses:
      200:
        description: Manilla modificada correctamente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Manilla no encontrada  
    """
    return edit_smart()

@smart_bp.route('/smart/asign', methods=['PUT'])
@token_required
@role_required([1])
def asign_a_smart():
    """
    Asignar una manilla existente
    ---
    tags:
      - Manillas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: AsignmentSmart
          required:
            - user_id
            - smart_id
          properties:
            user_id:
              type: integer
              description: ID del usuario asignado
            smart_id:
              type: integer
              description: ID de la manilla  
    responses:
      200:
        description: Manilla asignada correctamente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Manilla no encontrada  
    """
    return asign_smart()

@smart_bp.route('/smart/delete/<int:smart_id>', methods=['DELETE'])
@token_required
@role_required([1])
def delete_smart(smart_id):
    """
    Eliminar una manilla existente
    ---
    tags:
      - Manillas
    parameters:
      - name: smart_id
        in: path
        type: integer
        required: true
        description: ID de la manilla a eliminar
    responses:
      200:
        description: Manilla eliminada exitosamente
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      404:
        description: Manilla no encontrada
    """  
    return remove_smart(smart_id)