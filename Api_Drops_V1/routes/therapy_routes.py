from flask import Blueprint
from ..controllers.therapy_controller import (
    list_therapies, 
    insert_therapy, 
    list_balances, list_nurses, list_patients,
    info_therapy
)

therapy_bp = Blueprint('therapy',__name__)

therapy_bp.route('/api/therapies', methods=['GET'])(list_therapies)
therapy_bp.route('/api/therapy/create',methods=['POST'])(insert_therapy)
therapy_bp.route('/api/therapy/patients', methods=['GET'])(list_patients)
therapy_bp.route('/api/therapy/nurses',methods=['GET'])(list_nurses)
therapy_bp.route('/api/therapy/balances',methods=['GET'])(list_balances)
therapy_bp.route('/api/therapy/info/<int:therapy_id>',methods=['GET'])(info_therapy)