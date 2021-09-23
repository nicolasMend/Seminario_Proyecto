import pytest

from app import create_app
from app.db import create_all, drop_all, db
from app.products.models import Product, Category
from app.products.views import create_product_form
from conf.config import TestingConfig

from flask import template_rendered


@pytest.fixture
def app():
    app = create_app(config=TestingConfig)
    with app.app_context():
        create_all()
        app.teardown_bkp = app.teardown_appcontext_funcs
        app.teardown_appcontext_funcs = []
        yield app
        drop_all()

    return app


@pytest.fixture
def product(app):
    with app.app_context():
        product = Product(name="fake-product", price=1, description="hello",
                          refundable=True)
        db.session.add(product)
        db.session.commit()
        return product


@pytest.fixture
def category(app):
    with app.app_context():
        category = Category(name="fake-category")
        db.session.add(category)
        db.session.commit()
        return category


@pytest.fixture
def test_client(app):
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture
def captured_templates(app):
    """
    No comprendi la forma de enviar la platilla para el test desde aqui
    Documentacion: https://flask.palletsprojects.com/en/1.1.x/signals/
    """
    recorded = []

    def record(sender, template, context, **extra):
        template = create_product_form()
        recorded.append((template, context))
        template_rendered.connect(record, app)
        try:
            yield recorded
        finally:
            template_rendered.disconnect(record, app)
