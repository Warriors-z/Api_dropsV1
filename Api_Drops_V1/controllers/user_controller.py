from flask import abort, jsonify, request
import bcrypt
import random
import string
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Metodo para cifrar la contraseña usando bcrypt
def encrypt_password(password):
    #Generar la el salt(semilla) para el cifrado
    salt = bcrypt.gensalt()
    
    #Cifrar la contraña usando el salt(semilla)
    encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return encrypted_password

# Metodo para verificar la contraseña
def verify_password(password,encrypted_password):
    return bcrypt.checkpw(password.encode('utf-8'), encrypted_password)

# Metodo para generar crendenciales del usuario
def generate_credentials(name, lastName):
    initials = name[0].lower() + lastName[0].lower()
    aleatory_number = random.randint(100000, 999999)

    username = f"{initials}{aleatory_number}"
    password = ''.join(random.choices(string.digits, k=8))

    return username, password

# Metodo para enviar al correo las credenciales del Usuario
async def send_credentials(name, lastName, destiny_email):
    username, password = generate_credentials(name, lastName)

    # Configurar el correo
    sender = os.getenv('SENDER')
    password_sender = os.getenv('PASSWORD_SENDER')
    affair = "Estas son tus credenciales para poder acceder al sistema DROPS."

    # Crear el contenido del correo
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = destiny_email
    message["Subject"] = affair

    body = f"""
    Hola {name} {lastName},

    Aquí tienes tus credenciales de acceso:

    Username: {username}
    Contraseña: {password}

    Por favor, asegúrate de cambiar tu contraseña al iniciar sesión.

    Saludos,
    Tu equipo de soporte
    """
    message.attach(MIMEText(body, "plain"))

    # Conectar al servidor de correo y enviar el correo de forma asíncrona
    try:
        await smtplib.send(
            message,
            hostname=os.getenv('SMTP'),
            port=int(os.getenv('PORT_SMTP')),
            start_tls=True,
            username=sender,
            password=password_sender,
        )
        print("Correo enviado exitosamente a", destiny_email)
    except Exception as e:
        print("Error al enviar el correo:", e)