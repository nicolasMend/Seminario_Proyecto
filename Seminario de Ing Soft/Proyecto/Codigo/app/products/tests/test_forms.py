from app.products.forms import CreateCategoryForm, CreateProductForm


def test_should_create_category_form(app):
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        form_category = CreateCategoryForm()
        print(">>>form_category: ", form_category)
        assert isinstance(form_category, CreateCategoryForm)


def test_should_create_product_form(app):
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        form_product = CreateProductForm()
        assert isinstance(form_product, CreateProductForm)
