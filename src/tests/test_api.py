from pyparsing import empty
from .. import api
from fastapi.testclient import TestClient

client = TestClient(api.app)

def test_get_login():
    response = client.get("/login")
    assert response.status_code == 200
    #assert response.html() == "empty"
