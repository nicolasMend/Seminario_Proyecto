from datetime import datetime
from app.products.models import Product, get_product_stock

from app.db import db


class RefOrderStatusCode(db.Model):
    order_status_code = db.Column(db.Integer, primary_key=True)
    order_status_decription = db.Column(db.String(100))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_status_code = db.Column(
        db.Integer, db.ForeignKey('ref_order_status_code.order_status_code'))
    date_created = db.Column(db.DateTime, default=datetime.now())
    order_details = db.Column(db.String(500))


class RefOrderItemStatusCode(db.Model):
    order_item_status_code = db.Column(db.Integer, primary_key=True)
    order_item_status_description = db.Column(db.String(100))


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order_item_status_code = db.Column(
        db.Integer, db.ForeignKey(
            'ref_order_item_status_code.order_item_status_code'))
    order_item_quantity = db.Column(db.Integer, nullable=False)
    order_item_price = db.Column(db.Integer, nullable=False)
    other_order_item_details = db.Column(db.String(500))


class RefInvoiceStatusCode(db.Model):
    invoice_status_code = db.Column(db.Integer, primary_key=True)
    invoice_status_description = db.Column(db.String(50), nullable=False)


class Invoice(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    invoice_status_code = db.Column(
        db.Integer, db.ForeignKey(
            'ref_invoice_status_code.invoice_status_code'))
    invoice_date = db.Column(db.DateTime, default=datetime.now())
    invoice_details = db.Column(db.String(500))


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.Integer, db.ForeignKey('invoice.number'))
    payment_date = db.Column(db.DateTime, default=datetime.now())
    payment_amount = db.Column(db.Integer, nullable=False)


def get_active_order(active_user):
    '''
    Verifica si el usuario actual tiene una orden, si la tiene verifica
    que este activa.
    '''
    # Obtiene ordenes, si no tiene sera None

    has_order = Order.query.filter_by(user_id=active_user.id).all()

    # Puede tener varias ordenes asi que busca la de estado activo (valor 2)
    if has_order:
        for active_order in has_order:
            if active_order.order_status_code == 2:
                return active_order

    active_order = None
    return active_order


def get_order_items(order):
    '''
    Obtiene los items de una orden
    '''
    order_products = OrderItem.query.filter_by(order_id=order.id).all()

    return order_products


def update_quantity_order(order_item_id, quantity):
    '''
    Actualizar la cantidad de un producto del carro de compras y el
    precio de los items.
    '''
    # Obtener el item de la orden
    item = OrderItem.query.filter_by(id=order_item_id).first()
    # Obtener el producto que corresponde a dicho item
    product = Product.query.filter_by(id=item.product_id).first()
    # Optener stock del producto
    stock = get_product_stock(product)

    if stock < quantity:
        return False

    item.order_item_quantity = quantity
    item.order_item_price = quantity*product.price

    db.session.commit()

    return True


def delete_item_order(order_item_id):
    '''
    Borrar producto de una orden
    '''
    item = OrderItem.query.filter_by(id=order_item_id).first()
    db.session.delete(item)
    db.session.commit()


def create_order(active_user_id):
    '''
    Crea una orden activa para un usuario
    '''
    new_order = Order(user_id=active_user_id,
                      order_status_code=2)
    db.session.add(new_order)
    if db.session.commit():
        return True

    return False


def add_item_order(order_id, product_id, quantity):
    '''
    Agrega item a una orden
    '''

    # Obtener todos los items de la orden
    order_items = OrderItem.query.filter_by(order_id=order_id).all()

    # Buscar si ya existe el que se quiere agregar, si existe suma la cantidad
    for item in order_items:
        if item.product_id == product_id:
            quantity = item.order_item_quantity + quantity
            print(">>>>Antes")
            if update_quantity_order(item.id, quantity):
                print(">>>>Aqui")
                return True
            return False
    print(">>>>Nuevo")
    # Si no existe agrega el item a al orden
    product = Product.query.filter_by(id=product_id).first()
    price = product.price * quantity
    new_item = OrderItem(product_id=product_id, order_id=order_id,
                         order_item_status_code=2,
                         order_item_quantity=quantity, order_item_price=price)
    db.session.add(new_item)
    db.session.commit()

    return True
