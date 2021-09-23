from flask import Blueprint, request, render_template, redirect, url_for
from app.order.models import (
    get_active_order,
    get_order_items,
    update_quantity_order,
    delete_item_order
)
from app.products.models import get_order_products
from flask_login import login_required, current_user

order = Blueprint("order", __name__, url_prefix="")


@order.route('/shop_cart', methods=['GET', 'POST'])
@login_required
def show_shop_cart():
    '''
    method GET = Obtiene los productos de una orden y los pasa al template
    para ser mostrados, obtiene tambien el costo de la orden y la cantidad
    de productos
    methos POST = Actualiza la cantidad de articulos del carrito
    '''

    # obtener es estado de la orden (activa)
    active_order = get_active_order(current_user)
    # Si es activa obtiene los items que componene la orden()

    if active_order:
        order_items = get_order_items(active_order)
        if order_items:
            order_products = get_order_products(order_items)
        else:
            order_products = None
            order_items = None
    else:
        order_products = None
        order_items = None

    if request.method == "GET":

        # Poner estas variables como vacias (no como None) y poder usar zip()
        if order_products is None or order_items is None:
            order_products = []
            order_items = []
        # Unir las consultas
        products = zip(order_items, order_products)
        # Costos para modulo de pago
        prices = []
        descriptions = []
        total = 0
        for item in order_items:
            prices.append(item)
            total += item.order_item_price
        for product in order_products:
            descriptions.append(product)
        values = products

        iva = total*0.19

        my_info = {"products": products, "values": values, "total": total,
                   "iva": iva}

    if request.method == "POST":
        order_item_id = int(request.form.get("order_item_id"))
        action = request.form.get("action")

        if action == "update":
            quantity = int(request.form.get("quantity"))
            update_quantity_order(order_item_id, quantity)

        elif action == "erase":
            delete_item_order(order_item_id)

        return redirect(url_for('order.show_shop_cart'))

    return render_template('shop_cart.html', my_info=my_info)
