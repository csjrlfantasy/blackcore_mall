from flask import Blueprint, request, jsonify
from flasgger import swag_from
from models import db, User
from services.discount import calculate_discount  # 导入折扣算法

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'amount': {'type': 'number', 'example': 50.0}
                },
                'required': ['amount']
            }
        }
    ],
    'responses': {
        200: {'description': 'Payment successful'},
        400: {'description': 'Insufficient balance or invalid token'}
    }
})
def payment_process():
    token = request.headers.get('Authorization')
    user = User.query.filter_by(token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 400

    data = request.json
    amount = data.get('amount')

    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    # 调用打折算法计算折扣
    amount, discount_rate = calculate_discount(amount)

    if user.balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    user.balance -= amount
    db.session.commit()

    return jsonify({"message": "Payment successful"}), 200
