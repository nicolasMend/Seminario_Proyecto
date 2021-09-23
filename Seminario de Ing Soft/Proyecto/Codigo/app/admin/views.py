from flask import Blueprint, request, render_template, \
    flash

from app.products.models import create_new_product

admin = Blueprint("admin", __name__, url_prefix='/admin')


@admin.route("/userinfo", methods=['GET', 'POST'])
def userinfo():
    pass


@admin.route("/add_product", methods=['GET', 'POST'])
def add_product():

    if request.method == 'POST':
        create_new_product(request.form["name"],
                           request.form["price"],
                           request.form["weight"],
                           request.form["description"],
                           request.form["refundable"],
                           request.form["category"],
                           request.form["image"])

        print(">>>>Refundable", request.form.get("refundable"))
        message = "Producto Creado"
        flash(message, 'success')

    return render_template('add_product.html',)
