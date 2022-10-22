# import db
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import status, Form
from fastapi.param_functions import Depends
from pydantic import BaseModel
from pydantic.errors import FrozenSetError
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def redirect_home(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin_home")
def admin_home(request: Request):
    
    return templates.TemplateResponse("adminHome.html", {"request": request})

@app.get("/admin_manage_users")
def admin_home(request: Request):
    
    return templates.TemplateResponse("adminManageUsers.html", {"request": request})

#Student functions
@app.post("/add_student")
def add_student(name: str = Form(...), password: str = Form(...), studentClass: str = Form(...), studentID: str = Form(...)):

    return db.add_student(name, password, studentClass, studentID)

@app.post("/login_student")
def login_student(username: str = Form(...), password: str = Form(...)):

    return db.login_student(username, password)

@app.post("/update_student")
def update_student(password: str = Form(...), studentClass: str = Form(...), studentID: str = Form(...)):

    return db.update_student(password, studentClass, studentID)

@app.post("/delete_student")
def delete_student(studentID):

    return db.delete_student(studentID)

#Admin function
@app.post("/add_admin")
def add_admin(name: str = Form(...), password: str = Form(...), controllingClass: str = Form(...), role: str = Form(...)):

    return db.add_admin(name, password, controllingClass, role)

@app.post("/login_admin")
def login_admin(username: str = Form(...), password: str = Form(...), role: str = Form(...)):

    return db.login_admin(username, password, role)

@app.post("/update_admin")
def update_admin(password: str = Form(...), controllingClass: str = Form(...), adminID: str = Form(...)):

    db.update_admin(password, controllingClass, adminID)

@app.post("/delete_admin")
def delete_admin(adminID: str = Form(...), role: str = Form(...)):

    return db.delete_admin(adminID, role)

#Classroom functions
@app.post("/add_classroom")
def add_classroom(name, controllingTeacher):

    return db.add_classroom(name, controllingTeacher)

@app.post("/get_classrooms")
def get_classrooms():

    return db.get_classrooms()

@app.post("/get_classroom_from_name")
def get_classroom_from_name(name):

    return db.get_classroom_object_from_name(name)

@app.post("/delete_classroom")
def delete_classroom(name):

    return db.delete_classroom(name)

#Message functions
def add_message(contents: str = Form(...), sentBy: str = Form(...), sentByID: str = Form(...), groupID: int = Form(...)):

    return db.add_message(contents, sentBy, sentByID, groupID)

def get_message():
    
    return db.get_message()


def get_message_from_time1_to_time2(time1: int = Form(...), time2: int = Form(...)):

    return db.get_message_from_time1_to_time2(time1, time2)

#Groups functions
def add_group(name: str = Form(...), classroomID: int = Form(...)):

    return db.add_group(name, classroomID)

def get_groups():

    return db.get_groups()

def delete_group(name: str = Form(...), classroomID: int = Form(...)):

    return db.delete_group(name, classroomID)

#Bullying request functions
def add_bullying_request(requestedBy: str = Form(...), requestedByID: str = Form(...), cause: str = Form(...), causeID: str = Form(...), controlledBy: str = Form(...), controlledByID: str = Form(...), completed: bool = Form(...)):

    return db.add_bullying_request(requestedBy, requestedByID, cause, causeID, controlledBy, controlledByID, completed)

def get_bullying_requests():

    return db.get_bullying_requests()

def update_bullying_request(state: bool = Form(...), requestedID: str = Form(...), causeID: str = Form(...)):

    db.update_bullying_request(state, requestedID, causeID)

