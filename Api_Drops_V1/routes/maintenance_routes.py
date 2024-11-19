from flask import Blueprint
from ..controllers.token_controller import token_required, role_required
from ..controllers.maintenance_controller import(
    insert_maintenance,
    maintenance_balance_by_code
)

maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/api/v1')

@maintenance_bp.route('/maintenance/create', methods=['POST'])
#@token_required
#@role_required([3])
def create_maintenance():
    """
    Registrar nuevo mantenimiento
    ---
    tags:
      - Mantenimientos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CreateMaintenance
          required:
            - balance_id
            - last_factor
            - user_id
          properties:
            balance_id:
              type: integer
              description: ID de la balanza
            last_factor:
              type: number
              format: double
              description: valor del factor de calibracion
            user_id:
              type: integer
              description: ID del usuario creador  
    responses:
      200:
        description: Mantenimiento registrado correctamente
      401: 
        description: Token de autenticación no válido
      403: 
        description: Permiso insuficiente
      404: 
        description: Registro no encontrado
    """
    return insert_maintenance()

@maintenance_bp.route('/maintenance/getBalance/<string:balance_code>', methods=['GET'])
#@token_required
#@role_required([3])
def get_balance_id_to_maintenance(balance_code):
    """
    Obtener el ID de la balanza a calibrar
    ---
    tags:
      - Mantenimientos
    parameters:
      - name: balance_code
        in: path
        type: string
        required: true
        description: CODIGO de la balanza
    responses:
      200:
        description: ID de la balanza a calibrar
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      500:
        description: Error interno del servidor
      400:
        description: Fallo en verificacion de la balanza
    """
    return maintenance_balance_by_code(balance_code)