from datetime import datetime
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    creation_date = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    orders = db.relationship("Order", backref='user_ref', lazy=True)
    user_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'user',  # Discriminator value for User instances
        'polymorphic_on': user_type  # Specifying which column to use for discrimination
    }

class Reseller(User):
    __tablename__ = 'resellers'
    company = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    website = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'reseller'  # Discriminator value for Admin instances
    }
class Admin(User):
    __tablename__ = 'admins'
    name = db.Column(db.String)
    title = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'admin'  # Discriminator value for Admin instances
    }
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String, db.ForeignKey('orders.id'), nullable=False)
    sequential_number = db.Column(db.Integer)
    product_code = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Product(db.Model): # product is to display in the catalog, and turns into an item when ordered
    code = db.Column(db.String, nullable=False, primary_key=True)
    description = db.Column(db.String)
    type = db.Column(db.String)
    available = db.Column(db.Boolean)
    price = db.Column(db.Float) # remember, Float is like a double

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    creation_date = db.Column(db.Date, default=datetime.utcnow())
    items = db.relationship('Item', backref='order', lazy=True) # I'm not sure about this one
    status = db.Column(db.String, default='new') # new, accepted, delivered, completed
    user = db.relationship('User', backref='orders_ref', lazy=True)

