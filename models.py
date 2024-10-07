from db import db  # 从 db 导入已初始化的 db 实例
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)  # 储存加密后的密码
    token = db.Column(db.String(120), unique=True, nullable=True)  # 登录后存储JWT token
    balance = db.Column(db.Float, default=0.0)  # 新增字段，用户余额
    role = db.Column(db.Integer, default=1)  # 权限字段，0为管理员，1为顾客

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 新增字段，订单创建时间

class FlashSaleOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purchase_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='flash_sale_orders')
    product = db.relationship('Product', backref='flash_sale_orders')

class DiscountConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    min_amount = db.Column(db.Float, nullable=False)  # 最小金额区间
    max_amount = db.Column(db.Float, nullable=False)  # 最大金额区间
    discount_rate = db.Column(db.Float, nullable=False)  # 折扣率，范围0-1