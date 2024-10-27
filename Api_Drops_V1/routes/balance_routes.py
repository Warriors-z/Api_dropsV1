from flask import Blueprint
from ..controllers.balance_controller import(
    list_balances,
    balance_by_id,
    insert_balance,
    edit_balance,
    remove_balance
)

balance_bp = Blueprint('balance',__name__)

balance_bp.route('/api/balances', methods=['GET'])(list_balances)
balance_bp.route('/api/balance/byId/<int:balance_id>', methods=['GET'])(balance_by_id)
balance_bp.route('/api/balance/create', methods=['POST'])(insert_balance)
balance_bp.route('/api/balance/update', methods=['PUT'])(edit_balance)
balance_bp.route('/api/balance/delete', methods=['PUT'])(remove_balance)