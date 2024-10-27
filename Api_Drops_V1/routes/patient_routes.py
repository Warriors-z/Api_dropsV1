from flask import Blueprint
from ..controllers.patient_controller import (
    list_patients,
    patient_by_id,
    inser_patient,
    edit_patient,
    remove_patient
)

patient_bp = Blueprint('patient',__name__)

patient_bp.route('/api/patients', methods=['GET'])(list_patients)
patient_bp.route('/api/patient/byId/<int:patient_id>', methods=['GET'])(patient_by_id)
patient_bp.route('/api/patient/create', methods=['POST'])(inser_patient)
patient_bp.route('/api/patient/update', methods=['PUT'])(edit_patient)
patient_bp.route('/api/patient/delete', methods=['PUT'])(remove_patient)