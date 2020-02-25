import json
import pytest
# import sys
# sys.path.append("..")

try:
    from pyroi.pyroi import app
except:
    from pyroi.pyroi import app

@pytest.fixture
def client():
    return app.test_client()

def test_response(client):
    result = client.get()
    response_body = json.loads(result.get_data())
    assert result.status_code == 200
    print(result.headers['Content-Type'])
    print(response_body['Output'])
    # assert result.headers['Content-Type'] == 'application/json'
    # assert response_body['Output'] == 'Hello World'
