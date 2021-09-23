from http import HTTPStatus
from flask import Blueprint, Response, request, render_template, redirect, \
    url_for, flash
from app.products.forms import (
    CreateCategoryForm,
    CreateProductForm
)
from app.products.models import (
    get_all_categories,
    create_new_category,
    get_all_products,
    get_product_by_id,
    get_category_products_by_id,
    create_new_product,
    add_stock
)

from app.order.models import (
    get_active_order,
    create_order,
    add_item_order
)

from flask_login import login_required, current_user

products = Blueprint("products", __name__, url_prefix='/products')

EMPTY_SHELVE_TEXT = "Empty shelve!"
PRODUCTS_TITLE = "<h1> Products </h1>"
DUMMY_TEXT = "Dummy method to show how Response works"
RESPONSE_BODY = {
    "message": "",
    "data": [],
    "errors": [],
    "metadata": []
}


@products.route('/dummy-product', methods=['GET', 'POST'])
@login_required
def dummy_product():
    """ This method test the request types. If is GET Type it will
    render the text Products in h1 label with code 500.
    If is POST Type it will return Empty shelve! with status code 403
    """
    if request.method == 'POST':
        return EMPTY_SHELVE_TEXT, HTTPStatus.FORBIDDEN

    return PRODUCTS_TITLE, HTTPStatus.INTERNAL_SERVER_ERROR


@products.route('/dummy-product-2')
@login_required
def dummy_product_two():
    """ This method shows how Response object could be used to make API
    methods.
    """
    return Response(DUMMY_TEXT, status=HTTPStatus.OK)


@products.route('/categories')
def get_categories():
    """
        Verificar que si get_all_categories es [] 400, message = "No hay nada"
    :return:
    """
    categories = get_all_categories()
    status_code = HTTPStatus.OK
    if categories:
        RESPONSE_BODY["message"] = "OK. Categories List"
        RESPONSE_BODY["data"] = categories
    else:
        RESPONSE_BODY["message"] = "OK. No categories found"
        RESPONSE_BODY["data"] = categories
        status_code = HTTPStatus.NOT_FOUND

    my_info = {"categories": categories, "status_code": status_code}

    return render_template('categories.html', my_info=my_info)


@products.route('/category/<int:id>')
def get_category_products(id):
    products = get_category_products_by_id(id)
    RESPONSE_BODY["data"] = products

    my_info = {"products": products}
    return render_template('category.html', my_info=my_info)


@products.route('/add-category', methods=['POST'])
@login_required
def create_category():
    """
    Agrega categoria a la base de datos
    :return:
    """
    RESPONSE_BODY["message"] = "Method not allowed"
    status_code = HTTPStatus.METHOD_NOT_ALLOWED
    if request.method == "POST":
        data = request.json
        category = create_new_category(data["name"])
        RESPONSE_BODY["message"] = "OK. Category created!"
        RESPONSE_BODY["data"] = category
        status_code = HTTPStatus.CREATED

    return RESPONSE_BODY, status_code


@products.route('/')
def get_products():
    products_obj = get_all_products()

    RESPONSE_BODY["data"] = products_obj
    RESPONSE_BODY["message"] = "Products list"

    return RESPONSE_BODY, 200


@products.route('/product/<int:id>', methods=['GET', 'POST'])
def get_product(id):
    '''
    GET method = renderiza el template de producto
    POST method = agrega el producto a la orden, si no hay orden se crea una
    '''
    if request.method == "POST":

        quantity = int(request.form.get("quantity"))

        active_order = get_active_order(current_user)

        if active_order is None:
            create_order(current_user.id)
            active_order = get_active_order(current_user)

        if add_item_order(active_order.id, id, quantity):
            # Mensaje
            flash("Producto Agregado", 'success')
        else:
            flash("Error al Agregar producto", 'error')

        return redirect(url_for('products.get_product', id=id))

    if request.method == "GET":
        product = get_product_by_id(id)
        RESPONSE_BODY["data"] = product
        my_info = {"product": product}

    return render_template('product.html', my_info=my_info)


@products.route('/product-stock/<int:id>')
def get_product_stock(product_id):
    pass


@products.route('/need-restock')
@login_required
def get_products_that_need_restock():
    pass


@products.route('/register-product-stock/<int:id>', methods=['PUT', 'POST'])
@login_required
def register_product_refund_in_stock(id):

    # TODO Complete this view to update stock for product when a register for
    # this products exists. If not create the new register in DB

    status_code = HTTPStatus.CREATED
    if request.method == "PUT":
        data = request.json
        stock = add_stock(id, data["quantity"])
        RESPONSE_BODY["message"] = \
            "Stock for this product were updated successfully!"
        status_code = HTTPStatus.OK
    elif request.method == "POST":
        data = request.json
        stock = add_stock(id, data["quantity"])
        RESPONSE_BODY["message"] = \
            "Stock for this product were created successfully!"
        RESPONSE_BODY["data"] = stock
        status_code = HTTPStatus.CREATED
    else:
        RESPONSE_BODY["message"] = "Method not Allowed"
        status_code = HTTPStatus.METHOD_NOT_ALLOWED
    return RESPONSE_BODY, status_code


@products.route('/create-category-form', methods=['GET', 'POST'])
@login_required
def create_category_form():
    form_category = CreateCategoryForm()
    if request.method == 'POST' and form_category.validate():
        create_new_category(name=form_category.name.data)
        return redirect(url_for('products.category_success'))

    return render_template('create_category_form.html', form=form_category)


@products.route('/create-category-form-old', methods=['GET', 'POST'])
@login_required
def create_category_form_old():
    if request.method == 'POST':
        category = create_new_category(request.form["name"])
        RESPONSE_BODY["message"] = "Se agrego la categoria {} con \
            exito".format(request.form["name"])
        RESPONSE_BODY["data"] = category
        status_code = HTTPStatus.CREATED
        return RESPONSE_BODY, status_code
    return render_template("create_category_form_old.html")


@products.route('/category_success')
@login_required
def category_success():
    return render_template('category_success.html')


@products.route('/create-product-form', methods=['GET', 'POST'])
@login_required
def create_product_form():
    form_product = CreateProductForm()
    if request.method == 'POST' and form_product.validate():
        if form_product.refundable.data == "1":
            form_product.refundable.data = True
        else:
            form_product.refundable.data = False
        create_new_product(name=form_product.name.data,
                           price=form_product.price.data,
                           weight=form_product.weight.data,
                           description=form_product.description.data,
                           refundable=form_product.refundable.data,
                           category_id=form_product.category_id.data,
                           image=form_product.image.data)
        return redirect(url_for('products.product_success'))

    return render_template('create_product_form.html', form=form_product)


@products.route('/create-product-form-old', methods=['GET', 'POST'])
@login_required
def create_product_form_old():
    if request.method == 'POST':
        product = create_new_product(request.form["name"],
                                     request.form["price"],
                                     request.form["weight"],
                                     request.form["description"],
                                     request.form["refundable"],
                                     request.form["category_id"],
                                     request.form["image"])
        RESPONSE_BODY["message"] = "Se agrego el producto {} con \
            exito".format(request.form["name"])
        RESPONSE_BODY["data"] = product
        status_code = HTTPStatus.CREATED
        return RESPONSE_BODY, status_code
    return redirect(url_for('admin.add_product'))


@products.route('/product_success')
@login_required
def product_success():
    return render_template('product_success.html')


'''------Vistas agregadas------'''


@products.route('/add-product', methods=['POST'])
@login_required
def create_product():
    """
    Agregar producto a la base de datos
    :return:
    """
    RESPONSE_BODY["message"] = "Method not allowed"
    status_code = HTTPStatus.METHOD_NOT_ALLOWED
    if request.method == "POST":
        data = request.json
        product = create_new_product(data["name"], data["price"],
                                     data["weight"], data["description"],
                                     data["refundable"], data["category_id"])
        RESPONSE_BODY["message"] = "OK. Product created!"
        RESPONSE_BODY["data"] = product
        status_code = HTTPStatus.CREATED

    return RESPONSE_BODY, status_code


@products.route('/show-catalog', methods=['GET'])
def show_products_catalog():
    products = get_all_products()
    my_info = {"products": products, "pygroup": "PyGroup 01", "Jeison": 9105}
    return render_template('catalog.html', my_info=my_info)
    # Consultar la BD y extraer todos los productos disponibles
    # Almacenar la informacion en una variable de contexto
    # Renderizar la plantilla que tengamos en HTML e insertar
    # los datos de nuestra variable de contexto
