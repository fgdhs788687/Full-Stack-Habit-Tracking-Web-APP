def test_ai_endpoint(client, auth_headers):
    message = {
        'message':'Can u name 10 books?'
    }

    ai_response = client.post('/chat/', headers=auth_headers, json=message)

    assert ai_response.status_code == 200
    assert isinstance(ai_response.json(), dict)
    assert isinstance(ai_response.json()['response'], str)
    assert len(ai_response.json()['response']) > 0