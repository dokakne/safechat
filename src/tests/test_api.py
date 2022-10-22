from pyparsing import empty
from .. import api
from fastapi.testclient import TestClient

client = TestClient(api.app)

def test_get_login():

    response = client.get("/login")
    assert response.status_code == 200
    
def test_post_login1():

    response = client.post("/login", data={"username": "LMAO", "password": "LMAO"})
    assert response.status_code == 200

def test_post_login2():

    response = client.post("/login", data={"username": "asdf", "password": "aa"})
    assert response.status_code == 401