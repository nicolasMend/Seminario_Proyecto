from app.db import db, ma
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(25))
    phone_number = db.Column(db.Integer)


class RefPaymentMethod(db.Model):
    payment_method_code = db.Column(db.Integer, primary_key=True)
    payment_method_description = db.Column(db.String(25))


class UserPaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payment_method_code = db.Column(
        db.Integer, db.ForeignKey('ref_payment_method.payment_method_code'))
    credit_card_number = db.Column(db.Integer)
    payment_method_details = db.Column(db.String(500), nullable=True)


class RefPaymentMethodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RefPaymentMethod
        fields = ["payment_method_code", "payment_method_description"]


def get_payment_methods():
    payment_methods = RefPaymentMethod.query.all()
    payment_methods_schema = RefPaymentMethodSchema()
    payment_methods = [payment_methods_schema.dump(
        payment_method) for payment_method in payment_methods]
    return payment_methods
