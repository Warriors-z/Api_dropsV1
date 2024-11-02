from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

def create_api_drops():
    api_drops_v1 = Flask(__name__)
    CORS(api_drops_v1)

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API Drops",
            "description": "Documentación de la API Drops con autenticación JWT",
            "version": "1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Introduce el token en el formato: Bearer <token>"
            }
        },
        "security": [{"Bearer": []}]
    }
    swagger = Swagger(api_drops_v1, template=swagger_template)

    # Rutas Terapia
    from.routes.therapy_routes import therapy_bp
    api_drops_v1.register_blueprint(therapy_bp)

    # Rutas Balanza
    from.routes.balance_routes import balance_bp
    api_drops_v1.register_blueprint(balance_bp)

    # Rutas Paciente
    from.routes.patient_routes import patient_bp
    api_drops_v1.register_blueprint(patient_bp)

    # Rutas Usuario
    from .routes.user_routes import user_bp
    api_drops_v1.register_blueprint(user_bp)

    return api_drops_v1