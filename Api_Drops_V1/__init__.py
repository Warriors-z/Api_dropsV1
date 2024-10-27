from flask import Flask
from flask_cors import CORS

def create_api_drops():
    api_drops_v1 = Flask(__name__)
    CORS(api_drops_v1)

    # Rutas Terapia
    from.routes.therapy_routes import therapy_bp
    api_drops_v1.register_blueprint(therapy_bp)

    # Rutas Balanza
    from.routes.balance_routes import balance_bp
    api_drops_v1.register_blueprint(balance_bp)

    # Rutas Paciente
    from.routes.patient_routes import patient_bp
    api_drops_v1.register_blueprint(patient_bp)

    return api_drops_v1