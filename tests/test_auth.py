def test_register_user(client):
    payload = {
        "email": "testuser@gmail.com",
        "password": "testuser123",
        "timezone": "Asia/Kolkata"
    }

    response = client.post('/auth/register', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == "testuser@gmail.com"
    assert data['timezone'] == "Asia/Kolkata"
    assert 'id' in data
    assert "password" not in data
    assert "hashed_password" not in data

def test_register_duplicate_email_fails(client):
    payload = {
        "email": "testuser@gmail.com",
        "password": "testuser123",
        "timezone": "Asia/Kolkata"
    }

    client.post('/auth/register', json=payload)

    second_response = client.post('/auth/register', json=payload)

    assert second_response.status_code == 400
    assert second_response.json()['detail'] == "User already exists"

def test_login_user(client):
    # Register a user first:
    payload = {
        "email": "testuser@gmail.com",
        "password": "testuser123",
        "timezone": "Asia/Kolkata"
    }

    response = client.post('/auth/register', json=payload)
    assert response.status_code == 201

    # Lets login the user:
    credentials = {
        "username":"testuser@gmail.com",
        "password": "testuser123"
    }

    login_response = client.post('/auth/login', data=credentials)

    assert login_response.status_code == 200
    data = login_response.json()
    assert 'access_token' in data
    assert data['token_type'] == "bearer"
    assert isinstance(data['access_token'], str)
    assert isinstance(data['token_type'], str)
    assert len(data['access_token']) > 0

def test_current_user_me(client):

    payload = {
        "email": "testuser@gmail.com",
        "password": "testuser123",
        "timezone": "Asia/Kolkata"
    }

    response = client.post('/auth/register', json=payload)
    assert response.status_code == 201

    login_response = client.post(
        '/auth/login',
        data = {"username": "testuser@gmail.com", "password": "testuser123"}
    )

    assert login_response.status_code == 200
    data = login_response.json()

    token = data['access_token']
    headers = {"Authorization" : f"Bearer {token}"}

    me_check = client.get('/auth/me', headers=headers)
    assert me_check.status_code == 200
    me_data = me_check.json()
    assert me_data['email'] == "testuser@gmail.com"
    assert me_data['timezone'] == "Asia/Kolkata"
    assert 'id' in me_data