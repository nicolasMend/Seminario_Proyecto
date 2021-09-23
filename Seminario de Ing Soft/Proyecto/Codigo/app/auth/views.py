from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db
from app.auth.models import (
    User, get_payment_methods,
    RefPaymentMethod,
    UserPaymentMethod
)

from flask_login import login_user, logout_user

auth = Blueprint("auth", __name__, url_prefix="")


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        # verificacion de credenciales
        user = User.query.filter_by(email=email).first()
        if user:
            password_validation = check_password_hash(user.password, password)
            if not password_validation:
                flash("Verifica tus credenciales he intenta de nuevo", 'error')
                return redirect(url_for("auth.login"))
            login_user(user, remember=remember)
            return redirect(url_for("index"))
        else:
            flash("Verifica tus credenciales he intenta de nuevo", 'error')
            return redirect(url_for("auth.login"))

    return render_template('login.html', login=True)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        address = request.form.get("address")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone_number")

        # Verificacion de usuario
        user = User.query.filter_by(email=email).first()
        if user:
            message = "ERROR! Ya existe este usuario"
            flash(message, 'error')
            return redirect(url_for('auth.signup'))

        hash_password = generate_password_hash(password)
        new_user = User(email=email, password=hash_password, address=address,
                        first_name=first_name, last_name=last_name,
                        phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        user_id = user.id

        # Obtener y añadir datos a ref_payment_method table
        payment_method = request.form.get("payment_method")
        ref_payment_method = RefPaymentMethod.query.filter_by(
            payment_method_description=payment_method).first()
        payment_method = ref_payment_method.payment_method_code

        credit_card_number = request.form.get("credit_card_number")

        user_pyment_method = UserPaymentMethod(
            user_id=user_id, payment_method_code=payment_method,
            credit_card_number=credit_card_number
        )
        db.session.add(user_pyment_method)
        db.session.commit()

        message = "Usuario Creado"
        flash(message, 'success')

        return redirect(url_for('auth.login'))

    if request.method == "GET":
        payment_methods = get_payment_methods()
        my_info = {"payment_methods": payment_methods,
                   "signup": True}

    return render_template('signup.html', my_info=my_info)
