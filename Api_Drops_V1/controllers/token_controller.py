from functools import wraps
from flask import request, jsonify
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token de autenticación es requerido."}), 401

        try:
            token = token.split(" ")
            if len(token) != 2 or token[0] != "Bearer":
                return jsonify({"message": "Formato de token inválido. Debe ser 'Bearer <token>'"}), 401
            
            token = token[1]
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            request.user = decoded_token
        except ExpiredSignatureError:
            return jsonify({"message": "El token ha expirado"}), 401
        except DecodeError:
            return jsonify({"message": "Token inválido o malformado"}), 401

        return f(*args, **kwargs)
    
    return decorated

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'user'):
                return jsonify({"message": "No autorizado."}), 403

            user_role = request.user.get("role_id")

            if user_role not in allowed_roles:
                return jsonify({"message": "Acceso denegado: permiso insuficiente."}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator