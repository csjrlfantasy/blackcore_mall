from flask import Blueprint, request, jsonify
from flasgger import swag_from
from models import db, User, Product, Order

create_order_bp = Blueprint('create_order', __name__)

@create_order_bp.route('/order', methods=['POST'])
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
                    'product_id': {'type': 'integer'},
                    'quantity': {'type': 'integer'}
                },
                'required': ['product_id', 'quantity']
            }
        }
    ],
    'responses': {
        201: {'description': 'Order created successfully'},
        400: {'description': 'Invalid token or insufficient stock or balance'}
    }
})
def create_order():
    token = request.headers.get('Authorization')
    user = User.query.filter_by(token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 400

    data = request.json
    product = Product.query.get(data['product_id'])

    if not product or product.stock < data['quantity']:
        return jsonify({"error": "Insufficient stock"}), 400

    total_amount = product.price * data['quantity']

    if user.balance < total_amount:
        return jsonify({"error": "Insufficient balance"}), 400

    user.balance -= total_amount  # 扣除余额
    product.stock -= data['quantity']  # 更新库存
    new_order = Order(product_id=product.id, user_id=user.id, quantity=data['quantity'])

    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order created successfully"}), 201
