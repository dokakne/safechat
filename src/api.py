from src import sqldb
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

@app.get("/login")
def get_login(request: Request):

    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin_dash")
def get_admin_dash(request: Request):

    return templates.TemplateResponse("adminDashboard.html", {"request": request})

@app.post("/login")
def post_login(request: Request, username: str = Form(...), password: str = Form(...)):

    student = sqldb.get_student_object_from_username_and_password(username, password)
    admin = sqldb.get_admin_object_from_username_and_password(username, password)
    if (student == sqldb.BLANK_STUDENT and admin == sqldb.BLANK_ADMIN):

        return RedirectResponse("/login?error=True", status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/students")
def get_students(request: Request):

    return sqldb.get_students()

@app.post("/add_student")
def post_add_student(name: str = Form(...), password: str = Form(...), studentClass: str = Form(...), DoB: str = Form(...), Address: str = Form(...), PhoneNumber: int = Form(...), studentID: int = Form(...)):

    sqldb.add_student(name, password, studentClass, DoB, Address, PhoneNumber, studentID)

@app.get("/get_students")
def get_students(request: Request):

    return sqldb.get_students()

@app.post("/delete_student")
def post_delete_student(studentID: int = Form(...)):

    sqldb.delete_student(studentID)

@app.get("/get_messages")
def get_messages():

    return sqldb.get_messages()

@app.get("/get_chats")
def get_chats(uid: int = Form(...)):

    return sqldb.get_messages_for_user(uid)

@app.post("/add_message")
def post_add_message(sender: str = Form(...), senderID: int = Form(...), receiverID: int = Form(...), message: str = Form(...)):

    sqldb.add_message(message, sender, senderID, receiverID)

@app.post("/report_bullying")
def post_report_bullying(sender: str = Form(...), senderID: int = Form(...), cause: str = Form(...), causeID: int = Form(...), controlledBy: str = Form(...), controlledByID: int = Form(...), completed: bool = Form(...)):

    sqldb.add_message(sender, senderID, cause, causeID, controlledBy, controlledByID, completed)

@app.post("/create_chat")
def post_create_chat(person1: str = Form(...), person1ID: str = Form(...), person2: str = Form(...), person2ID:str = Form(...), classroomID: int = Form(...)):

    sqldb.create_chat(person1, person1ID, person2, person2ID, classroomID)