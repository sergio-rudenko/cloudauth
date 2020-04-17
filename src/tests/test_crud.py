from app import conf

# CRUD -----------------------------------------------------------------------
# Endpoint	    HTTP Method	    CRUD Method	    Result
# /notes/	    GET	            READ	        get all notes
# /notes/:id/	GET	            READ	        get a single note
# /notes/	    POST	        CREATE	        add a note
# /notes/:id/	PUT	            UPDATE	        update a note
# /notes/:id/	DELETE	        DELETE	        delete a note

fake_user_lk_token = '01234567890123456789012345678901'
fake_user_phone = '+12345670000'
fake_user_email = 'user@host.zz'


def test_get_all_users(test_app):
    response = test_app.get(f'{conf.api_prefix}/users/',
                            params={'offset': 0, 'limit': 0},
                            headers={'X-Token': conf.ADMIN_TOKEN})
    assert response.status_code == 200
    assert response.text == '[]'


def test_get_all_users_wrong_admin_token(test_app):
    response = test_app.get(f'{conf.api_prefix}/users/',
                            params={'offset': 0, 'limit': 0},
                            headers={'X-Token': conf.USER_TOKEN})
    assert response.status_code == 401
    assert response.text == '{"detail":"admin token required"}'


def test_add_user(test_app):
    data = {
        "phone": fake_user_phone,
        "email": fake_user_email,
        "lk_token": fake_user_lk_token
    }
    response = test_app.post(f'{conf.api_prefix}/users/', json=data,
                             headers={'X-Token': conf.USER_TOKEN})
    assert response.text != ""
    assert response.status_code == 201

# def test_add_user_already_exists(test_app):
#     data = {"token": fake_user_token}
#     response = test_app.post(f'{conf.api_prefix}/users/', json=data,
#                              headers={'X-Token': conf.USER_TOKEN})
#     assert response.status_code == 401
#     assert response.text == '{"detail":"user already exists"}'


# def test_get_user_by_phome(test_app):
#     response = test_app.get(f'{conf.api_prefix}/users',
#                             params={'user_phone': fake_user_phone},
#                             headers={'X-Token': conf.USER_TOKEN})
#     assert response.status_code == 401
#     assert response.text == '{"detail":"admin token required"}'


#
#
# def test_add_user_empty_token(test_app):
#     fake_user_token = ''
#     response = test_app.post(f'{conf.api_prefix}/users/',
#                              data=f'"token":{fake_user_token}',
#                              headers={'X-Token': conf.USER_TOKEN})
#     assert response.status_code == 400
#
#
# def test_get_single_user(test_app):
#     response = test_app.get(f'{conf.api_prefix}/users/0/',
#                             headers={'X-Token': conf.USER_TOKEN})
#     assert response.status_code == 200
#     assert response.text == ''
#
#
# def test_get_single_user_wrong_hash(test_app):
#     response = test_app.get(f'{conf.api_prefix}/users/-1/',
#                             headers={'X-Token': conf.USER_TOKEN})
#     assert response.status_code == 400
#     assert response.text == '{"detail":"token required"}'
