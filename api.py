from fastapi import FastAPI
from fastapi import status, Form
from fastapi.param_functions import Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pydantic.errors import FrozenSetError
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
app.mount("/", StaticFiles(directory="templates"), name="templates")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
