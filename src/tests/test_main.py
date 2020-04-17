from app import conf


def test_message(test_app):
    response = test_app.get(f'{conf.api_prefix}/test', headers={'X-Token': '12345678'})
    assert response.status_code == 200
    assert response.text == '{"message":"Hello, World!"}'


def test_message_failed(test_app):
    response = test_app.get(f'{conf.api_prefix}/test', headers={'X-Token': ''})
    assert response.status_code == 401
    assert response.text == '{"detail":"token required"}'
