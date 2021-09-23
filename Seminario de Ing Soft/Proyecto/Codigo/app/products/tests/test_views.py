from http import HTTPStatus


def test_should_resturn_200_when_requesting_categories(app, test_client,
                                                       category):
    with app.app_context():
        result = test_client.get('/products/categories')
        assert result.status_code == HTTPStatus.OK


def test_should_resturn_404_found_when_requesting_categories(app,
                                                             test_client):
    with app.app_context():
        result = test_client.get('/products/categories')
        assert result.status_code == HTTPStatus.NOT_FOUND
