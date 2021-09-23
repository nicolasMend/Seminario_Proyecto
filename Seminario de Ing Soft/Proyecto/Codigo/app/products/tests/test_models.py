import pytest

from app.products.models import (get_product_by_id,
                                 create_new_category,
                                 Category)
from app.products.exceptions import ProductNotFoundError


def test_should_get_product_id_when_product_exists_in_db(app, product):
    with app.app_context():
        result = get_product_by_id(product.id)
        assert result["name"] == product.name


def test_should_get_product_id_when_product_does_not_exists_in_db(app):
    with pytest.raises(ProductNotFoundError):
        with app.app_context():
            get_product_by_id(12)


def test_should_create_new_category(app):
    with app.app_context():
        category = create_new_category(name="Test")
        assert isinstance(category, Category) is True
