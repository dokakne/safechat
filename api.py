from db import *
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

@app.get("/login_student")
def redirect_login_student(request: Request):

    return templates.TemplateResponse("loginStudent.html", {"request": request})

@app.post("/login_post_student")
def login_post(username: str = Form(...), password: str = Form(...)):

    loginResponse = login_student(username, password)

    if (loginResponse != BLANK_STUDENT):
    
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    else:
        
        return RedirectResponse("/login_student?error=True", status_code=status.HTTP_302_FOUND)


@app.get("/login_admin")
def redirect_login_admin(request: Request):

    return templates.TemplateResponse("loginAdmin.html", {"request": request})

@app.post("/login_post_admin")
def login_post(username: str = Form(...), password: str = Form(...)):

    loginResponse = login_admin(username, password)

    if (loginResponse != BLANK_ADMIN):
    
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    else:
        
        return RedirectResponse("/login_admin?error=True", status_code=status.HTTP_302_FOUND)