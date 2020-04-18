import pytest


def test_path(test_app):
    response = test_app.get('/')
    assert response.status_code == 200
    print(response.text)


@pytest.mark.parametrize("headers, status_code, text", [
    ({'X-Token': 'not_empty_token'}, 200, '{"message":"Hello, World!"}'),
    ({'X-Token': ''}, 401, '{"detail":"token required"}'),
    ({}, 422, ''),
])
def test_message(test_app, headers, status_code, text):
    response = test_app.get('/test', headers=headers)
    assert response.status_code == status_code
    if response.status_code != 422:
        assert response.text == text
