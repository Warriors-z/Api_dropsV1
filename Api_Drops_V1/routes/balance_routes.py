from flask import Blueprint
from ..controllers.token_controller import token_required, role_required
from ..controllers.balance_controller import(
    list_balances,
    balance_by_id,
    insert_balance,
    edit_balance,
    remove_balance,
    verify_exist_balance_code
)

balance_bp = Blueprint('balance',__name__, url_prefix='/api/v1')

@balance_bp.route('/balances', methods=['GET'])
@token_required
@role_required([1])
def get_balances():
    """
    Obtener lista de balanzas
    ---
    tags:
      - Balanzas  
    responses:
      200:
        description: Lista de balanzas
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Lista de balanzas no encontrada.  
    """
    return list_balances()

@balance_bp.route('/balance/byId/<int:balance_id>', methods=['GET'])
@token_required
@role_required([1])
def get_balance_by_id(balance_id):
    """
    Obtener balanza por ID
    ---
    tags:
      - Balanzas
    parameters:
      - name: balance_id
        in: path
        type: integer
        required: true
        description: ID de la balanza  
    responses:
      200:
        description: Datos de la balanza
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Balanza no encontrada  
    """
    return balance_by_id(balance_id)

@balance_bp.route('/balance/checkExist/<string:balance_code>', methods=['GET'])
@token_required
@role_required([1,3])
def verify_exist_balance(balance_code):
    """
    Verificar si existe la balanza
    ---
    tags:
      - Balanzas
    parameters:
      - name: balance_code
        in: path
        type: string
        required: true
        description: CODIGO de la balanza
    responses:
      200:
        description: Datos de la balanza
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      500:
        description: Error interno del servidor
      400:
        description: Fallo en verificacion de la balanza
    """
    return verify_exist_balance_code(balance_code)

@balance_bp.route('/balance/create', methods=['POST'])
@token_required
@role_required([1])
def create_balance():
    """
    Crear nueva balanza
    ---
    tags:
      - Balanzas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CreateBalance
          required:
            - balance_code
            - user_id
          properties:
            balance_code:
              type: string
              description: Codigo de la balanza
            user_id:
              type: integer
              description: ID del usuario creador  
    responses:
      200:
        description: Balanza creada correctamente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Balanza no encontrada  
    """
    return insert_balance()

@balance_bp.route('/balance/update', methods=['PUT'])
@token_required
@role_required([1])
def modify_balance():
    """
    Actualizar una balanza existente
    ---
    tags:
      - Balanzas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UpdateBalance
          required:
            - balance_code
            - user_id
            - balance_id
          properties:
            balance_code:
              type: string
              description: Codigo de la balanza
            user_id:
              type: integer
              description: ID del usuario modificador
            balance_id:
              type: integer
              description: ID de la balanza  
    responses:
      200:
        description: Balanza modificada correctamente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Balanza no encontrada  
    """
    return edit_balance()

@balance_bp.route('/balance/delete', methods=['DELETE'])
@token_required
@role_required([1])
def delete_balance():
    """
    Eliminar una balanza existente
    ---
    tags:
      - Balanzas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: DeleteBalance
          required:
            - user_id
            - balance_id
          properties:
            user_id:
              type: integer
              description: ID del usuario eliminador
            balance_id:
              type: integer
              description: ID de la balanza a eliminar 
    responses:
      200:
        description: Balanza eliminada exitosamente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Balanza no encontrada  
    """
    return remove_balance()