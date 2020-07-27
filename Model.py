from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields

ma = Marshmallow()
db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    product_code = db.Column(db.String(20), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, description, product_code, brand, price):
        self.name = name
        self.description = description
        self.product_code = product_code
        self.brand = brand
        self.price = price


class ProductSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String()
    product_code = fields.String(required=True)
    brand = fields.String(required=True)
    price = fields.Float(required=True)
