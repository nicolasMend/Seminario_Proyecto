from http import HTTPStatus


def test_should_return_template_create_category_form(app, test_client):
    """
    Verifica si la plantilla genera los componentes al solicutar su url,
    buscando algos de los datos que deben aparece y verificando
    que se aroje HTTPStatus.OK
    """
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        result = test_client.get('/products/create-category-form')
        assert b'Crear Categoria' in result.data
        assert b'<input id="name"' in result.data
        assert b'Name' and b'Ir' in result.data
        assert result.status_code == HTTPStatus.OK


def test_should_return_template_category_success(app, test_client):
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        result = test_client.get('/products/category_success')
        assert b'Categoria creada exitosamente!' in result.data
        assert result.status_code == HTTPStatus.OK


def test_should_return_template_create_product_form(app, test_client):
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        result = test_client.get('/products/create-product-form')
        assert b'Crear Producto' in result.data
        assert result.status_code == HTTPStatus.OK


def test_should_return_template_product_success(app, test_client):
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        result = test_client.get('/products/product_success')
        assert b'Producto creado exitosamente!' in result.data
        assert result.status_code == HTTPStatus.OK


def bad_test_should_return_template_product_success2(app, test_client,
                                                     captured_templates):
    """
    Encontre esta forma de hacer test a plantillas pero no logre entender la
    forma de enviar la plantilla en "captured_templates"
    """
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        with captured_templates(app) as templates:
            result = test_client.get('/products/create-product-form')
            assert result.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'create_category_form.html'
            assert len(context['items']) == 10
