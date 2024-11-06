from flask import Blueprint
from ..controllers.token_controller import token_required, role_required
from ..controllers.user_controller import(
    list_users,
    user_by_id,
    insert_user,
    edit_user,
    remove_user,
    verify_credentials
)

user_bp = Blueprint('user', __name__, url_prefix='/api/v1')

@user_bp.route('/users', methods=['GET'])
#@token_required
#@role_required([1]) # Solo administradores pueden acceder
def get_users():
    """
    Obtener lista de usuarios
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """
    return list_users()

@user_bp.route('/user/byId/<int:user_id>', methods=['GET'])
#@token_required
#@role_required([1])
def get_user_by_id(user_id):
    """
    Obtener usuario por ID
    ---
    tags:
      - Usuarios
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID del usuario
    responses:
      200:
        description: Datos del usuario
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
    """
    return user_by_id(user_id)

@user_bp.route('/user/create', methods=['POST'])
#@token_required
#@role_required([1])
def create_user():
    """
    Crear un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CreateUser
          required:
            - name
            - last_name
            - second_last_name
            - phone
            - email
            - address
            - birth_date
            - genre
            - ci
            - role_id
          properties:
            name:
              type: string
              description: Nombre del usuario
            last_name:
              type: string
              description: Apellido Paterno del usuario
            second_last_name:
              type: string
              description: Apellido Materno del usuario
            phone:
              type: string
              description: Telefono del usuario
            email:
              type: string
              description: Correo electrónico del usuario
            address:
              type: string
              description: Direccion del usuario
            birth_date:
              type: string
              description: Fecha de nacimiento del usuario
            genre:
              type: string
              description: Genero del usuario
            ci:
              type: string
              description: Carnet de identidad del usuario
            role_id:
              type: integer
              description: Rol del usuario
    responses:
      201:
        description: Usuario creado exitosamente
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      400:
        description: Error en los datos enviados
    """
    return insert_user()

@user_bp.route('/user/update', methods=['PUT'])
#@token_required
#@role_required([1])
def modify_user():
    """
    Actualizar un usuario existente
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UpdateUser
          required:
            - user_id
            - name
            - last_name
            - second_last_name
            - phone
            - email
            - address
            - birth_date
            - genre
            - ci
            - role_id
          properties:
            user_id:
              type: integer
              description: ID del usuario
            name:
              type: string
              description: Nombre del usuario
            last_name:
              type: string
              description: Apellido Paterno del usuario
            second_last_name:
              type: string
              description: Apellido Materno del usuario
            phone:
              type: string
              description: Telefono del usuario
            email:
              type: string
              description: Correo electrónico del usuario
            address:
              type: string
              description: Direccion del usuario
            birth_date:
              type: string
              description: Fecha de nacimiento del usuario
            genre:
              type: string
              description: Genero del usuario
            ci:
              type: string
              description: Carnet de identidad del usuario
            role_id:
              type: integer
              description: Rol del usuario
    responses:
      200:
        description: Usuario actualizado exitosamente
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      400:
        description: Error en los datos enviados
    """
    return edit_user()

@user_bp.route('/user/delete/<int:user_id>', methods=['DELETE'])
#@token_required
#@role_required([1])
def delete_user(user_id):
    """
    Eliminar un usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID del usuario a eliminar
    responses:
      200:
        description: Usuario eliminado exitosamente
      401:
        description: Token de autenticación no válido
      403:
        description: Permiso insuficiente
      404:
        description: Usuario no encontrado
    """
    return remove_user(user_id)

@user_bp.route('/credentials', methods=['POST'])
def login():
    """
    Verificación de Credenciales
    ---
    tags:
      - Autenticación
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Login
          required:
            - user_id
            - username
            - password
            - role_id
          properties:
            username:
              type: string
              description: Nombre de usuario
            password:
              type: string
              description: Contraseña del usuario
            user_id: 
                type: integer
                description: ID del usuario
            role_id:
                type: integer
                description: Rol del Usuario
    responses:
      200:
        description: Credenciales válidas y retorno de token
      404:
        description: Credenciales inválidas
    """
    return verify_credentials()