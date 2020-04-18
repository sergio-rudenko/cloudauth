import pytest

from app import conf

# CRUD -----------------------------------------------------------------------
# Endpoint	    HTTP Method	    CRUD Method	    Result
# /notes/	    GET	            READ	        get all notes
# /notes/:id/	GET	            READ	        get a single note
# /notes/	    POST	        CREATE	        add a note
# /notes/:id/	PUT	            UPDATE	        update a note
# /notes/:id/	DELETE	        DELETE	        delete a note

fake_data1 = {
    'key': '0123456789',
    'description': 'test data',
    'user_phone': '+12345678000',
}

fake_data2 = {
    'key': '9876543210',
    'description': 'fake data #1 for cascade deletion',
    'user_phone': '+12345678000',
}

fake_data3 = {
    'key': 'ABCDEFGHIJ',
    'description': 'fake data #2 for cascade deletion',
    'user_phone': '+12345678000',
}


@pytest.mark.parametrize("path, token, status_code, text", [
    ('/users/', conf.USER_TOKEN, 401, '{"detail":"Admin Token Required"}'),
    ('/users/', conf.ADMIN_TOKEN, 200, '[]'),

    ('/tokens/', conf.USER_TOKEN, 401, '{"detail":"Admin Token Required"}'),
    ('/tokens/', conf.ADMIN_TOKEN, 200, '[]'),

    ('/hashes/', conf.USER_TOKEN, 401, '{"detail":"Admin Token Required"}'),
    ('/hashes/', conf.ADMIN_TOKEN, 200, '[]'),
])
def test_get_all_as_admin(test_app, path, token, status_code, text):
    response = test_app.get(f'{conf.api_prefix}{path}',
                            params={'offset': 0, 'limit': 0},
                            headers={'X-Token': token})
    assert response.status_code == status_code
    assert response.text == text


@pytest.mark.parametrize("path, data, token, status_code, text", [
    ('/tokens/', fake_data1, 'incorrect user token', 401, '{"detail":"Not Authorised"}'),
    ('/tokens/', fake_data1, conf.USER_TOKEN, 201, ''),
    ('/tokens/', fake_data1, conf.USER_TOKEN, 409, '{"detail":"Already Exists"}'),

    ('/hashes/', fake_data1, 'incorrect user token', 401, '{"detail":"Not Authorised"}'),
    ('/hashes/', fake_data1, conf.USER_TOKEN, 201, ''),
    ('/hashes/', fake_data1, conf.USER_TOKEN, 409, '{"detail":"Already Exists"}'),

    # more records for the records throne...
    ('/tokens/', fake_data2, conf.USER_TOKEN, 201, ''),
    ('/tokens/', fake_data3, conf.USER_TOKEN, 201, ''),
    ('/hashes/', fake_data2, conf.USER_TOKEN, 201, ''),
    ('/hashes/', fake_data3, conf.USER_TOKEN, 201, ''),
])
def test_create_user_token_or_hash(test_app, path, data, token, status_code, text):
    response = test_app.post(f'{conf.api_prefix}{path}', json=data,
                             headers={'X-Token': token})
    assert response.status_code == status_code
    if response.status_code != 201:
        assert response.text == text


@pytest.mark.parametrize("token, params, status_code, text", [
    (conf.USER_TOKEN, {'phone': fake_data1['user_phone']}, 401, '{"detail":"Admin Token Required"}'),
    (conf.ADMIN_TOKEN, {'phone': fake_data1['user_phone']}, 200, ''),
    (conf.ADMIN_TOKEN, {'phone': 'incorrect phone'}, 404, '{"detail":"Not Found"}'),

    (conf.USER_TOKEN, {'lk_token': fake_data1['key']}, 200, ''),
    (conf.USER_TOKEN, {'lk_token': 'incorrect token'}, 404, '{"detail":"Not Found"}'),

    (conf.USER_TOKEN, {'auth_hash': fake_data1['key']}, 200, ''),
    (conf.USER_TOKEN, {'auth_hash': 'incorrect hash'}, 404, '{"detail":"Not Found"}'),

    (conf.ADMIN_TOKEN, {}, 400, '{"detail":"Parameter Required"}'),
    (conf.USER_TOKEN, {}, 400, '{"detail":"Parameter Required"}'),
])
def test_read_user(test_app, token, params, status_code, text):
    response = test_app.get(f'{conf.api_prefix}/user', params=params,
                            headers={'X-Token': token})
    assert response.status_code == status_code
    if response.status_code != 200:
        assert response.text == text


@pytest.mark.parametrize("path, key, token, status_code, text", [
    ('/hashes/', fake_data1['key'], 'incorrect user token', 401, '{"detail":"Not Authorised"}'),
    ('/hashes/', fake_data1['key'], conf.USER_TOKEN, 204, 'null'),
    ('/hashes/', fake_data1['key'], conf.USER_TOKEN, 404, '{"detail":"Not Found"}'),

    ('/tokens/', fake_data1['key'], 'incorrect user token', 401, '{"detail":"Not Authorised"}'),
    ('/tokens/', fake_data1['key'], conf.USER_TOKEN, 204, 'null'),
    ('/tokens/', fake_data1['key'], conf.USER_TOKEN, 404, '{"detail":"Not Found"}'),

    ('/users/', fake_data1['user_phone'], conf.USER_TOKEN, 401, '{"detail":"Admin Token Required"}'),
    ('/users/', fake_data1['user_phone'], conf.ADMIN_TOKEN, 204, "null"),
    ('/users/', fake_data1['user_phone'], conf.ADMIN_TOKEN, 404, '{"detail":"Not Found"}'),
])
def test_delete_user_token_or_hash(test_app, path, key, token, status_code, text):
    response = test_app.delete(f'{conf.api_prefix}{path}{key}/', headers={'X-Token': token})
    assert response.status_code == status_code
    assert response.text == text
