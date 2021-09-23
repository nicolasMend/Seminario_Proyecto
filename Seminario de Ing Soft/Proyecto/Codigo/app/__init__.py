from flask import Flask, render_template
from flask_wtf import CSRFProtect

from app.auth.models import User
from app.auth.views import auth
from app.order.views import order
from app.admin.views import admin
from app.db import db, ma
from conf.config import DevelopmentConfig
from app.products.views import products
from app.products.models import (
    get_last_products,
    get_random_categories,
    get_all_categories
)
from flask_migrate import Migrate
from flask_login import LoginManager

ACTIVE_ENDPOINTS = [
    ("/products", products), ("", auth), ("", order), ("/admin", admin)]


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)
    app.config.from_object(config)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Ingrese para acceder a esta pagina."

    login_manager.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ruta principal de la pagina
    @app.route('/', methods=['GET'])
    def index():
        last_products = get_last_products()
        random_cat = get_random_categories()
        categories = get_all_categories()
        my_info = {"products": last_products,
                   "random_cat": random_cat, 
                   "categories": categories}
        return render_template("index.html", my_info=my_info)

    # Varables globales para ser usadas en cualquier plantilla
    @app.context_processor
    def global_variables():
        categories = get_all_categories()
        basics = {"categories": categories}
        return dict(basics=basics)

    return app


if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run()
