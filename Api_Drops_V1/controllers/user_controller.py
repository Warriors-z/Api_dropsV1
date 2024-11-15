from flask import abort, jsonify, request
import bcrypt
import jwt
import datetime
import random
import string
import asyncio
import os
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from ..schemas.login_schema import LoginSchema, ValidationError
from ..schemas.user_schema import UserInsertSchema, UserUpdateSchema, ValidationError
from ..models.dtos.user_dto import User
from ..models.user import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    check_credentials,
    check_exists_user,
)

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Metodo para cifrar la contraseña usando bcrypt
def encrypt_password(password):
    #Generar la el salt(semilla) para el cifrado
    salt = bcrypt.gensalt()
    
    #Cifrar la contraña usando el salt(semilla)
    encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return encrypted_password

# Creacion del Token
def create_jwt_token( username, role_id, expires_in=3600):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=expires_in);
    payload = {
        "username": username,
        "role_id": role_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

# Metodo para verificar la contraseña
def verify_credentials():
    data = request.get_json()
    if not data:
        abort(404, description="Error: No se proporcionaron las crendenciales.")

    try: 
        validated_data = LoginSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400  

    username = validated_data['username']
    password = validated_data['password']
    role_id = validated_data['role_id']
    credentials = check_credentials(username)
    

    if credentials and isinstance(credentials, dict):
        is_valid = bcrypt.checkpw(password.encode('utf-8'), credentials['password'].encode('utf-8'))

        if username == credentials['username'] and is_valid and role_id == credentials['idRole']:
            access_token = create_jwt_token(username, role_id)
            return jsonify({
                "message": "Credenciales Válidas.",
                "access_token": access_token, 
                "role_id": credentials['idRole'],
                "user_id": credentials['idUser']
            }), 200

    return jsonify({"message": "Credenciales Inválidas."}), 404
    
# Metodo para generar crendenciales del usuario
def generate_credentials(name, last_name):
    initials = name[0].lower() + last_name[0].lower()
    aleatory_number = random.randint(100000, 999999)

    username = f"{initials}{aleatory_number}"
    password = ''.join(random.choices(string.digits, k=8))

    return username, encrypt_password(password), password

# Metodo para enviar al correo las credenciales del Usuario
async def send_credentials(name, last_name, destiny_email, username, password):
    # Configurar el correo
    sender = os.getenv('SENDER')
    password_sender = os.getenv('PASSWORD_SENDER')
    smtp_server = os.getenv('SMTP')
    smtp_port = int(os.getenv('PORT_SMTP'))
    affair = "Estas son tus credenciales para poder acceder al sistema DROPS."

    # Crear el contenido del correo
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = destiny_email
    message["Subject"] = affair

    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333333;
                background-color: #f4f4f9;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            h2 {{
                color: #4a90e2;
            }}
            .content {{
                line-height: 1.6;
                font-size: 16px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 14px;
                color: #666666;
                text-align: center;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                margin-top: 20px;
                color: #ffffff;
                background-color: #4a90e2;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Hola, {name} {last_name}</h2>
            <div class="content">
                <p>¡Bienvenido! Aquí tienes tus credenciales de acceso al sistema:</p>
                <p><strong>Usuario:</strong> {username}<br>
                <strong>Contraseña:</strong> {password}</p>
                <p>Por favor, asegúrate de cambiar tu contraseña al iniciar sesión para proteger tu cuenta.</p>
                <a href="https://www.tusitio.com/login" class="button">Ir a la página de inicio de sesión</a>
            </div>
            <div class="footer">
                <p>Saludos,<br>
                El equipo de soporte.</p>
                <p>Este correo es confidencial y solo debe ser usado por el destinatario.</p>
            </div>
        </div>
    </body>
    </html>
    """
    message.attach(MIMEText(body, "html"))

    # Conectar al servidor de correo y enviar el correo de forma asíncrona
    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_server,
            port=smtp_port,
            start_tls=True,
            username=sender,
            password=password_sender,
        )
        print("Correo enviado exitosamente a", destiny_email)
    except Exception as e:
        print("Error al enviar el correo:", e)

def list_users():
    users = get_all_users()
    if users is None:
        abort(404, description="Error: Registros no encontrados.")
    return jsonify(users)

def user_by_id(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        abort(404, description="Error: Registro no encontrado.")
    return jsonify(user)

def check_exists_user_ci(ci):
    exist_ci = check_exists_user(ci)
    if exist_ci is not None:
        return jsonify({"ci":exist_ci})
    return jsonify({"ci":exist_ci})

def insert_user():
    data = request.get_json()


    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    try:
        validated_user_data = UserInsertSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    name = validated_user_data['name']
    last_name = validated_user_data['last_name']
    second_last_name = validated_user_data['second_last_name'] or ''
    phone = validated_user_data['phone'] or ''
    email = validated_user_data['email']
    address = validated_user_data['address']
    birth_date = validated_user_data['birth_date']
    genre = validated_user_data['genre']
    ci = validated_user_data['ci']
    role_id = validated_user_data['role_id']

    

    username, password, password_to_send = generate_credentials(name, last_name)

    if not all([name, last_name,email,address,birth_date, genre, ci, role_id, phone]):
        abort(400, description="Error: Faltan datos necesarios para la creacion del Usuario.")


    user = User(name, last_name, email, address, birth_date, genre, ci, second_last_name,role_id, phone,user_id=None, user_name=username, password=password)

    ci_exists = check_exists_user(ci)

    if ci_exists is not None: 
        abort(400, description="El usuario ya está registrado.")

    if not create_user(user):
        abort(500, description="Error: Fallo interno del servidor.")

    asyncio.run(send_credentials(name, last_name, email, username, password_to_send))
    return jsonify({
        "message": "Creacion exitosa del Usuario."
    }), 201

def edit_user():
    try:
        data = request.get_json()

        print(data)
    except Exception as e:
        abort(400, description="Error de formato JSON: " + str(e))

    if not data:
        abort(400, description="Error: No se proporcionaron datos.")

    try:
        validated_user_data = UserUpdateSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = validated_user_data['user_id']
    name = validated_user_data['name']
    last_name = validated_user_data['last_name']
    second_last_name = validated_user_data['second_last_name'] or ''
    phone = validated_user_data['phone'] or ''
    email = validated_user_data['email']
    address = validated_user_data['address']
    birth_date = validated_user_data['birth_date']
    genre = validated_user_data['genre']
    ci = validated_user_data['ci']
    role_id = validated_user_data['role_id']

    if not all([user_id, name, last_name, email,address, birth_date, ci, role_id]):
        abort(400, description="Error: Faltan datos necesarios para la edicion del Usuario")

    user = User(name, last_name, email, address, birth_date, genre, ci,second_last_name, role_id, phone,user_id)

    new_user = update_user(user)

    if not new_user:
        abort(500, description="Error: Fallo interno del servidor")
    return jsonify({
        "message": "Edicion exitosa."
    }), 200

def remove_user(user_id):
    if user_id is None:
        abort(400, description="Error: Falta el ID del usuario a eliminar")

    user = delete_user(user_id)

    if not user:
        abort(500, description="Error: Fallo interno del servidor.")
    return jsonify({
        "message": "Elimanacion de Usuario exitosa!"
    }), 200