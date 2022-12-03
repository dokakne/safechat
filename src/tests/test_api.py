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

def test_get_admin_dash():

    response = client.get("/admin_dash")
    assert response.status_code == 200

def test_get_students():

    response = client.get("/get_students")
    assert response.status_code == 200

def test_post_add_student():

    response = client.post("/add_student", data={"name": "Test", "password": "Test", "studentClass": "Test", "DoB": "Test", "Address": "Test", "PhoneNumber": 123, "studentID": 123})
    assert response.status_code == 200

def test_delete_student():

    response = client.post("/delete_student", data={"studentID": 123})
    assert response.status_code == 200

def test_add_admin():

    response = client.post("/add_admin", data={"name": "Test", "password": "Test", "controllingClass": "Test", "adminID": 123, "role": "Teacher"})
    assert response.status_code == 200

def test_get_admins():

    response = client.get("/get_admins")
    assert response.status_code == 200

def test_delete_admin():

    response = client.post("/delete_admin", data={"adminID": 123})
    assert response.status_code == 200

def test_get_messages():

    response = client.get("/get_messages")
    assert response.status_code == 200

def test_get_chats():

    response = client.get("/get_chats", data={"uid": 1})
    assert response.status_code == 200

def test_post_add_message():

    response = client.post("/add_message", data={"sender": "Test", "senderID": 1, "receiverID": 1, "message": "Test"})
    assert response.status_code == 200

def test_report_bullying():

    response = client.post("/report_bullying", data={"sender": "Test", "senderID": 1, "cause": "Test", "causeID": 1, "controlledBy": "Test", "controlledByID": 1, "completed": True})
    assert response.status_code == 200

def test_create_chat():

    response = client.post("/create_chat", data={"person1": "Test", "person1ID": 1, "person2": "Test", "person2ID": 1, "classroomID": 1})
    assert response.status_code == 200

def test_get_calendar():

    response = client.get("/calendar", data={"personID": 1})
    assert response.status_code == 200

def test_get_tasks():

    response = client.post("/tasks_per_person", data={"personID": -1})
    print(response.text)
    assert response.status_code == 200

def test_add_calendar_event():

    response = client.post("/add_calendar_event", data={"personID": "1", "event": "Test", "date": "Test"})
    assert response.status_code == 200

def test_add_task():

    response = client.post("/add_task", data={"personID": "Test", "title": "Test", "completed": True})
    assert response.status_code == 200

def test_delete_calendar_event():

    response = client.post("/delete_calendar_event", data={"dbID": 1})
    assert response.status_code == 200


def test_delete_task():

    response = client.post("/delete_task", data={"personID": "1", "title": "Test"})
    assert response.status_code == 200

def test_complete_task():

    response = client.post("/complete_task", data={"completed": True, "personID": "132", "title":"Test"})
    print(response.text)
    assert response.status_code == 200

def test_add_class():

    response = client.post("/add_class", data={"name": "Test", "controllingTeacher": "Test"})
    assert response.status_code == 200

def test_get_classes():

    response = client.get("/get_classes")
    assert response.status_code == 200