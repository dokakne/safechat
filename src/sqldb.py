import psycopg2
import time
import urllib.parse as urlparse 
from pydantic import BaseModel
from jose import jwt, JWTError
import os
from passlib.context import CryptContext
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.getenv("DATABASE_URL"))
conn = psycopg2.connect(database=url.path[1:],
  user=url.username,
  password=url.password,
  host=url.hostname,
  port=url.port
)

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):

    return pwd_context.hash(password)

class Student(BaseModel):

    name: str
    password: str
    studentClass: str
    studentID: str
    DoB: str
    Address: str
    PhoneNumber: int
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

    person1: str
    person1ID: str
    person2: str
    person2ID: str
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

class Calendar(BaseModel):

    personID: str
    Title: str
    Date: int
    dbID: int

class Task(BaseModel):

    personID: str
    Title: str
    completed: bool
    dbID: int

BLANK_STUDENT = Student(name="", password="", studentClass="", studentID=-1, DoB="", Address="", PhoneNumber=-1, dbID=-1)
BLANK_ADMIN = Admin(name="", password="", controllingClass="", dbID=-1, adminID=-1, role="")
BLANK_CLASSROOM = Classroom(name="", dbID=-1, controllingTeacher="")
BLANK_MESSAGE = Message(contents="", sentBy="", sentByID=-1, timeSent=0, groupID=-1)
BLANK_GROUP = Group(person1="", person1ID="", person2="", person2ID="", dbID=-1, classroomID=-1)
BLANK_BULLYING_REQUEST = BullyingRequest(requestedBy="", requestedByID="", cause="", causeID="", controlledBy="", controlledByID="", dbID=-1, completed=False)
BLANK_CALENDAR = Calendar(personID="", Title="", Date=0, dbID=-1)
BLANK_TASK = Task(personID="", Title="", completed=False, dbID=-1)


def get_last_id(arr):

    return int(arr[-1].dbID)

def cursor_func(function, fetch):
    
    cursor = conn.cursor()
    cursor.execute(function)
    if (fetch):
        records = cursor.fetchall()
        return records
    
    conn.commit()

def add_base():

    cursor_func(f"INSERT INTO STUDENTS (name, password, studentClass, studentID, DoB, Address, PhoneNumber, dbID) VALUES ('LMAO', '{hash_password('LMAO')}', 'NOCLASS', '-1', 'NODOB', 'Bannnana Lane', 321489, 0)", False)
    cursor_func(f"INSERT INTO ADMINS (name, password, controllingClass, dbID, adminID, role) VALUES ('LMAO', '{hash_password('LMAO')}', 'NOCLASS', -1, -1, 'NOROLE')", False)
    cursor_func(f"INSERT INTO CLASSROOMS (name, dbID, controllingClass) VALUES ('LMAO', -1, 'LMAO')", False)
    cursor_func(f"INSERT INTO GROUPS (person1, person1ID, person2, person2ID, dbID, classroomID) VALUES ('LMAO', 'LMAO', 'LMAO', 'LMAO', -1, -1)", False)
    cursor_func(f"INSERT INTO MESSAGES (contents, sentBy, sentByID, timeSent, groupID) VALUES ('LMAO', 'LMAO', -1, -1, -1)", False)
    cursor_func(f"INSERT INTO BULLYING_REQUESTS (requestedBy, requestedByID, cause, causeID, controlledBy, controlledByID, dbID, completed) VALUES ('LMAO', '-1', 'LMAO', '-1', 'LMAO', '-1', -1, FALSE)", False)
    cursor_func(f"INSERT INTO CALENDARS (personID, Title, Date, dbID) VALUES ('LMAO', 'LMAO', -1, -1)", False)
    cursor_func(f"INSERT INTO TASKS (personID, Title, completed, dbID) VALUES ('LMAO', 'LMAO', FALSE, -1)", False)
def clear_tables():

    cursor_func("DELETE FROM STUDENTS;",False)
    cursor_func("DELETE FROM ADMINS;",False)
    cursor_func("DELETE FROM CLASSROOMS;",False)
    cursor_func("DELETE FROM GROUPS;",False)
    cursor_func("DELETE FROM MESSAGES;",False)
    cursor_func("DELETE FROM BULLYING_REQUESTS;",False)
    cursor_func("DELETE FROM CALENDARS;",False)
    cursor_func("DELETE FROM TASKS;",False)

#Student functions
def create_students():

    cursor_func("CREATE TABLE IF NOT EXISTS STUDENTS (name TEXT, password TEXT, studentClass TEXT, studentID INTEGER, DoB TEXT, Address TEXT, PhoneNumber INTEGER, dbID INTEGER)", False)

def add_student(name, password, studentClass, DoB, Address, PhoneNumber, studentID):

    dbID = get_last_id(get_students()) + 1
    cursor_func(f"INSERT INTO STUDENTS (name, password, studentClass, studentID, DoB, Address, PhoneNumber, dbID) VALUES ('{name}', '{hash_password(password)}', '{studentClass}', '{studentID}', '{DoB}', '{Address}', {PhoneNumber},'{dbID}')", False)
    return dbID

def get_students():

    studnets = cursor_func("SELECT * FROM STUDENTS", True)
    arr = []
    for i in studnets:

        ii = list(i)
        arr.append(Student(name=ii[0], password=ii[1], studentClass=ii[2], studentID=ii[3], DoB=ii[4], Address=ii[5], PhoneNumber=ii[6], dbID=ii[7]))
    return arr

def get_student_object_from_username_and_password(username, password):

    students = get_students()
    for student in students:
        
        if (student.name == username and (pwd_context.verify(password, student.password))):

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

    cursor_func(f"INSERT INTO ADMINS (name, password, controllingClass, dbID, adminID, role) VALUES ('{name}', '{hash_password(password)}', '{controllingClass}', '{get_last_id(get_admins()) + 1}', '{adminID}', '{role}')", False)

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

        if (admin.name == username and (pwd_context.verify(password, admin.password))):

            return add_admin
    
    return BLANK_ADMIN

def login_admin(username, password):

    return get_admin_object_from_username_and_password(username, password)

def update_admin(password, controllingClass, adminID):

    #The password and controllingClass is what we want changed
    #We use adminID to find the admin

    cursor_func(f"UPDATE ADMINS SET password='{password}', controllingClass='{controllingClass}' WHERE adminID='{adminID}';", False)

def delete_admin(adminID):

    cursor_func(f"DELETE FROM ADMINS WHERE adminID='{adminID}'", False)

#Classroom functions
def create_classrooms():

    cursor_func("CREATE TABLE IF NOT EXISTS CLASSROOMS (name TEXT, dbID INTEGER, controllingClass TEXT)", False)

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

#Message functions
def create_message_tables():

    cursor_func("CREATE TABLE IF NOT EXISTS MESSAGES (contents TEXT, sentBy TEXT, sentByID TEXT, timeSent TEXT, groupID TEXT)", False)
def add_message(contents, sentBy, sentByID, groupID):

    cursor_func(f"INSERT INTO MESSAGES (contents, sentBy, sentByID, timeSent, groupID) VALUES ('{contents}', '{sentBy}', '{sentByID}', '{int(time.time())}', '{groupID}')", False)

def get_messages():

    massages = cursor_func("SELECT * FROM MESSAGES", True)
    arr= []
    for i in massages:
            
        ii = list(i)
        arr.append(Message(contents=ii[0], sentBy=ii[1], sentByID=ii[2], timeSent=ii[3], groupID=ii[4]))
    
    return arr

def get_message_from_time1_to_time2(time1, time2):

    messages_arr = []
    for i in get_messages():
        if i.timeSent >= time1 and i.timeSent <= time2:

            messages_arr.append(i)
            next(i)

    return messages_arr

def get_messages_for_user(UID):

    messages = cursor_func(f"SELECT * FROM MESSAGES WHERE sentByID='{UID}'", True)

    print(messages)

#Group functions
def create_group_tables():

    cursor_func("CREATE TABLE IF NOT EXISTS GROUPS (person1 TEXT, person1ID TEXT, person2 TEXT, person2ID TEXT, dbID INTEGER, classroomID INTEGER)", False)

def get_groups():

    greps = cursor_func("SELECT * FROM GROUPS", True)
    arr = []
    for i in greps:
                
        ii = list(i)
        arr.append(Group(person1=ii[0], person1ID=ii[1], person2=ii[2], person2ID=ii[3], dbID=ii[4], classroomID=ii[5]))
    
    return arr

def add_group(person1, person1ID, person2, person2ID, classroomID):

    cursor_func(f"INSERT INTO GROUPS (person1, person1ID, person2, person2ID, dbID, classroomID) VALUES ('{person1}', '{person1ID}', '{person2}', '{person2ID}', '{get_last_id(get_groups()) + 1}', '{classroomID}')", False)


def get_group_object_from_classroom_id(classroomID):

    for group in get_groups():

        if (group.classroomID == classroomID):

            return group
    
    return BLANK_GROUP

def delete_group(person1, classroomID):

    cursor_func(f"DELETE FROM GROUPS WHERE person1='{person1}' AND classroomID='{classroomID}'", False) 

#Bullying request functions
def create_bullying_request_tables():

    cursor_func("CREATE TABLE IF NOT EXISTS BULLYING_REQUESTS (requestedBy TEXT, requestedByID TEXT, cause TEXT, causeID TEXT, controlledBy TEXT, controlledByID TEXT, dbID INT, completed BOOLEAN)", False)

def get_bullying_requests():

    bellying = cursor_func("SELECT * FROM BULLYING_REQUESTS", True)
    arr = []
    for i in bellying:

        ii = list(i)
        arr.append(BullyingRequest(requestedBy=ii[0], requestedByID=ii[1], cause=ii[2], causeID=ii[3], controlledBy=ii[4], controlledByID=ii[5], dbID=ii[6], completed=ii[7]))
    
    return arr
def add_bullying_request(requestedBy, requestedByID, cause, causeID, controlledBy, controlledByID, completed):

    cursor_func(f"INSERT INTO BULLYING_REQUESTS (requestedBy, requestedByID, cause, causeID, controlledBy, controlledByID, dbID, completed) VALUES ('{requestedBy}', '{requestedByID}', '{cause}', '{causeID}', '{controlledBy}', '{controlledByID}', {get_last_id(get_bullying_requests()) + 1}, {completed})", False)

def get_bullying_request_by_requestedID_and_causeID(requestedID, causeID):

    for request in get_bullying_requests():
            
        if (request.requestedByID == requestedID and request.causeID == causeID):

            return request
    
    return BLANK_BULLYING_REQUEST

def update_bullying_request(state, requestedID, causeID):

    cursor_func(f"UPDATE BULLYING_REQUESTS SET completed='{state}' WHERE requestedByID='{requestedID}' AND causeID='{causeID}'", False)

#Calendar funtions
def create_calendar_tables():

    cursor_func("CREATE TABLE IF NOT EXISTS CALENDARS (personID TEXT, Title TEXT, DATE INT, dbID INT)", False)

def get_calendars():

    celendars = cursor_func("SELECT * FROM CALENDARS", True)
    arr = []
    for i in celendars:

        ii = list(i)
        arr.append(Calendar(personID=ii[0], Title=ii[1], Date=ii[2], dbID=ii[3]))

    return arr

def create_calendar_event(personID, title, date):

    cursor_func(f"INSERT INTO CALENDARS (personID, Title, DATE, dbID) VALUES ('{personID}', '{title}', '{int(time.time())}', '{get_last_id(get_calendars()) + 1}')", False)

def delete_calendar_event(personID, title):

    cursor_func(f"DELETE FROM CALENDARS WHERE personID='{personID}' AND Title='{title}'", False)

def get_calendar_event_from_personID(personID):

    for event in get_calendars():

        if (event.personID == personID):

            return event
    
    return BLANK_CALENDAR

def update_calendar_event(Title, dbID):

    cursor_func(f"UPDATE CALENDARS SET Title='{Title}' WHERE dbID='{dbID}'", False)

def delete_calendar_event_from_dbID(dbID):

    cursor_func(f"DELETE FROM CALENDARS WHERE dbID='{dbID}'", False)

#Task functions
def create_task_tables():

    cursor_func("CREATE TABLE IF NOT EXISTS TASKS (personID TEXT, Title TEXT, Completed BOOLEAN, dbID INT)", False)

def get_tasks():

    tesks = cursor_func("SELECT * FROM TASKS", True)
    arr = []
    for i in tesks:

        ii = list(i)

        arr.append(Task(personID=ii[0], Title=ii[1], completed=ii[2], dbID=ii[3]))

    return arr

def create_task(personID, title, completed):

    cursor_func(f"INSERT INTO TASKS (personID, Title, Completed, dbID) VALUES ('{personID}', '{title}', '{completed}', '{get_last_id(get_tasks()) + 1}')", False)

def delete_task(personID, title):

    cursor_func(f"DELETE FROM TASKS WHERE personID='{personID}' AND Title='{title}'", False)

def get_task_from_personID(personID):

    for task in get_tasks():

        if (task.personID == personID):

            return task
    
    return BLANK_TASK

def update_task_title(Title, dbID):

    cursor_func(f"UPDATE TASKS SET Title='{Title}' WHERE dbID='{dbID}", False)

def update_task_completed(Completed, personID, Title):

    cursor_func(f"UPDATE TASKS SET Completed='{Completed}' WHERE personID='{personID}' AND Title='{Title}'", False)

def delete_task_from_dbID(dbID):

    cursor_func(f"DELETE FROM TASKS WHERE dbID='{dbID}'", False)

add_base()