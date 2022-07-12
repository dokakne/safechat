from pydantic import BaseModel
from jose import jwt, JWTError
import os
from passlib.context import CryptContext
from datetime import date, datetime, timedelta

SECRET_KEY = os.environ.get("APP_SECRET_KEY", "DefaultKey")
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash_password(password: str) -> str:
    
    return pwd_context.hash(password)

print(hash_password("AAAA"))

class Student(BaseModel):

    name: str
    password: str
    studentClass: str
    studentID: int
    dbID: int
    
class Admin(BaseModel):

    name: str
    password: str
    controllingClass: str
    role: str
    dbID: int

BLANK_STUDENT = Student(name="", password="", studentClass="", studentID=-1, dbID=-1)
BLANK_ADMIN = Admin(name="", password="", controllingClass="", role="", dbID=-1)

students = [Student(name="iamname", password="iampassword", studentClass="nope", studentID=0, dbID=0)]
admins = [Admin(name="iamname", password="iampassword", controllingClass="Nope", role="Nope", dbID=0)]

def get_last_id(arr):

    return arr[-1].dbID

#Student functions
def add_student(name, password, studentClass, studentID):

    students.append(Student(name=name, password=password, studentClass=studentClass, studentID=studentID, dbID=get_last_id(students) + 1))

def get_students():

    return students

def get_student_object_from_username_and_password(username, password):

    for student in students:

        if (student.name == username and student.password == password):

            return student
    
    return BLANK_STUDENT

def login_student(username, password):


    return get_student_object_from_username_and_password(username, password)

#Admin functions
def add_admin(name, password, controllingClass, role):

    admins.append(Admin(name=name, password=password, controllingClass=controllingClass, role=role, dbID=get_last_id(admins) + 1))

def get_admins():

    return admins

def get_admin_object_from_username_password(username, password):

    for admin in admins:

        if (admin.name == username and admin.password == password):

            return admin
    
    return BLANK_ADMIN

def login_admin(username, password):

    return get_admin_object_from_username_password(username, password)

add_student("Pratyush", "LMAO", "7E", "400")
add_admin("Mrs. Beck", "Ilovetomatoes", "8F", "Teacher")