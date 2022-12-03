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


@app.post("/add_student")
def post_add_student(name: str = Form(...), password: str = Form(...), studentClass: str = Form(...), DoB: str = Form(...), Address: str = Form(...), PhoneNumber: int = Form(...), studentID: int = Form(...)):

    dbID = sqldb.add_student(name, password, studentClass, DoB, Address, PhoneNumber, studentID)
    return dbID

@app.get("/get_students")
def get_students(request: Request):

    return sqldb.get_students()

@app.post("/delete_student")
def post_delete_student(studentID: int = Form(...)):

    sqldb.delete_student(studentID)

@app.post("/add_admin")
def post_add_admin(name: str = Form(...), password: str = Form(...), controllingClass: str = Form(...), adminID: int = Form(...), role: str = Form(...)):

    return sqldb.add_admin(name, password, controllingClass, adminID, role)

@app.get("/get_admins")
def get_admins(request: Request):

    return sqldb.get_admins()

@app.post("/delete_admin")
def post_delete_admin(adminID: int = Form(...)):
    
    return sqldb.delete_admin(adminID)

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
    
    print(completed)
    sqldb.add_bullying_request(sender, senderID, cause, causeID, controlledBy, controlledByID, completed)

@app.post("/create_chat")
def post_create_chat(person1: str = Form(...), person1ID: str = Form(...), person2: str = Form(...), person2ID:str = Form(...), classroomID: int = Form(...)):

    sqldb.add_group(person1, person1ID, person2, person2ID, classroomID)

@app.get("/calendar")
def get_calendar(personID: str = Form(...)):

    return sqldb.get_calendar_event_from_personID(personID)

@app.post("/tasks_per_person")
def get_task_from_personID(personID: str = Form(...)):

    return sqldb.get_task_from_personID(personID)

@app.post("/add_calendar_event")
def post_add_calendar_event(personID: str = Form(...), event: str = Form(...), date: str = Form(...)):

    sqldb.create_calendar_event(personID, event, date)

@app.post("/add_task")
def add_task(personID: str = Form(...), title: str = Form(...), completed: bool = Form(...)):

    sqldb.create_task(personID, title, completed)

@app.post("/delete_calendar_event")
def delete_calendar_event(dbID: int = Form(...)):

    sqldb.delete_calendar_event_from_dbID(dbID)

@app.post("/delete_task")
def delete_task(personID: str = Form(...), title: str = Form(...)):

    sqldb.delete_task(personID, title)

@app.post("/complete_task")
def complete_task(completed: bool = Form(...), personID: str = Form(...), title: str = Form(...)):

    sqldb.update_task_completed(completed, personID, title)