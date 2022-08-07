import psycopg2
import time
from pydantic import BaseModel
from jose import jwt, JWTError
import os
from passlib.context import CryptContext
from datetime import date, datetime, timedelta

SECRET_KEY = os.environ.get("APP_SECRET_KEY", "DefaultKey")
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
conn = psycopg2.connect("user=postgres password=safechat")

def hash_password(password: str) -> str:
    
    return pwd_context.hash(password)

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
    dbID: int
    adminID: str
    role: str

class Classroom(BaseModel):

    name: str
    dbID: int
    controllingTeacher: str

class Group(BaseModel):

    name: str
    dbID: int
    classroomID: int

class Message(BaseModel):

    contents: str
    sentBy: str
    sentByID: str
    timeSent: int
    groupID: int

class BullyingRequest(BaseModel):

    requestedBy: str
    requestedByID: str
    cause: str
    causeID: str
    controlledBy: str
    controlledByID: str
    dbID: int
    completed: bool

BLANK_STUDENT = Student(name="", password="", studentClass="", studentID=-1, dbID=-1)
BLANK_ADMIN = Admin(name="", password="", controllingClass="", dbID=-1, adminID=-1, role="")
BLANK_CLASSROOM = Classroom(name="", dbID=-1, controllingTeacher="")
BLANK_MESSAGE = Message(contents="", sentBy="", sentByID=-1, timeSent=0, groupID=-1)
BLANK_GROUP = Group(name="", dbID=-1, classroomID=-1)
BLANK_BULLYING_REQUEST = BullyingRequest(requestedBy="", requestedByID="", cause="", causeID="", controlledBy="", controlledByID="", dbID=-1, completed=False)


def get_last_id(arr):

    return arr[-1].dbID

def cursor_func(function, fetch):
    
    cursor = conn.cursor()
    cursor.execute(function)
    if (fetch):
        records = cursor.fetchall()
        return records
    
    conn.commit()

def add_base():

    cursor_func(f"INSERT INTO STUDENTS (name, password, studentClass, studentID, dbID) VALUES ('LMAO', 'LMAO', 'NOCLASS', '-1', '0')", False)
    cursor_func(f"INSERT INTO ADMINS (name, password, controllingClass, dbID, adminID, role) VALUES ('LMAO', 'LMAO', 'NOCLASS', '-1', '-1', 'NOROLE')", False)

def clear_tables():

    cursor_func("DELETE FROM STUDENTS;",False)

#Student functions
def create_students():

    cursor_func("CREATE TABLE IF NOT EXISTS STUDENTS (name TEXT, password TEXT, studentClass TEXT, studentID INTEGER, dbID INTEGER)", False)

def add_student(name, password, studentClass, studentID):

    cursor_func(f"INSERT INTO STUDENTS (name, password, studentClass, studentID, dbID) VALUES ('{name}', '{password}', '{studentClass}', '{studentID}', '{get_last_id(get_students()) + 1}')", False)

def get_students():

    studnets = cursor_func("SELECT * FROM STUDENTS", True)
    arr = []
    for i in studnets:

        ii = list(i)
        arr.append(Student(name=ii[0], password=ii[1], studentClass=ii[2], studentID=ii[3], dbID=ii[4]))
    return arr

def get_student_object_from_username_and_password(username, password):

    students = get_students()
    for student in students:

        if (student.name == username and student.password == password):

            return student
    
    return BLANK_STUDENT

def login_student(username, password):

    return get_student_object_from_username_and_password(username, password)

def update_student(password, studentClass, studentID):

    #The password and studentClass is what we want changed
    #We use studentID to find the student

    cursor_func(f"UPDATE STUDENTS SET password='{password}', studentClass='{studentClass}' WHERE studentID='{studentID}';", False)

def delete_student(studentID):

    cursor_func(f"DELETE FROM STUDENTS WHERE studentID='{studentID}'", False)


#Admin functions
def create_admin():

    cursor_func("CREATE TABLE IF NOT EXISTS ADMINS (name TEXT, password TEXT, controllingClass TEXT, dbID INTEGER, adminID TEXT, role TEXT)", False)
    
def add_admin(name, password, controllingClass, adminID, role):

    cursor_func(f"INSERT INTO ADMINS (name, password, controllingClass, dbID, adminID, role) VALUES ('{name}', '{password}', '{controllingClass}', '{get_last_id(get_admins()) + 1}'), '{adminID}', '{role}'", False)

def get_admins():

    admens = cursor_func("SELECT * FROM ADMINS", True)
    arr = []
    for i in admens:

        ii = list(i)
        arr.append(Admin(name = ii[0], password =  ii[1], controllingClass = ii[2], dbID = ii[3], adminID = ii[4], role = ii[5]))
    return arr

def get_admin_object_from_username_and_password(username, password):

    admins = get_students()
    for admin in admins:

        if (admin.name == username and admin.password == password):

            return add_admin
    
    return BLANK_ADMIN

def login_admin(username, password):

    return get_admin_object_from_username_and_password(username, password)

def update_admin(password, controllingClass, adminID):

    #The password and controllingClass is what we want changed
    #We use adminID to find the admin

    cursor_func(f"UPDATE ADMINS SET password='{password}', controllingClass='{controllingClass}' WHERE adminID='{adminID}';", False)

def deleteAdmin(adminID):

    cursor_func(f"DELETE FROM ADMINS WHERE adminID='{adminID}'", False)

#Classroom functions
def create_classrooms():

    cursor_func("CREATE TABLE IF NOT EXISTS CLASSROOMS (name TEXT, dbID INTEGER, controllingClass, TEXT)", False)

def add_classroom(name, controllingTeacher):

    cursor_func(f"INSERT INTO CLASSROOMS (name, dbID, controllingClass) VALUES ('{name}', '{get_last_id(get_classrooms() + 1)}', '{controllingTeacher}'", False)

def get_classrooms():

    classrems = cursor_func("SELECT * FROM CLASSROOMS")
    arr = []
    for i in classrems:
        
        ii = list(i)
        arr.append(Classroom(ii[0], ii[1], ii[2]))

    return arr


def get_classroom_object_from_name(name):

    for classroom in get_classrooms():

        if (classroom.name == name):

            return classroom
    
    return BLANK_CLASSROOM

def delete_classroom(name):

    cursor_func(f"DELETE FROM CLASSROOMS WHERE name='{name}'", False)
