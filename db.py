import time
from pydantic import BaseModel
from jose import jwt, JWTError
import os
from passlib.context import CryptContext
from datetime import date, datetime, timedelta

SECRET_KEY = os.environ.get("APP_SECRET_KEY", "DefaultKey")
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

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
BLANK_MESSAGE = Message(contents="", sentBy="", sentByID=-1, timeSent=0)
BLANK_GROUP = Group(name="", dbID=-1, classroomID=-1)
BLANK_BULLYING_REQUEST = BullyingRequest(requestedBy="", requestedByID="", cause="", causeID="", controlledBy="", controlledByID="", dbID=-1, completed=False)

students = [Student(name="iamname", password="iampassword", studentClass="nope", studentID=0, dbID=0)]
admins = [Admin(name="iamname", password="iampassword", controllingClass="Nope", dbID=0, adminID="admin-1", role="Nope")]
classrooms = [Classroom(name="iamname", dbID=0, controllingTeacher="iamteacher")]
groups = [Group(name="iamname", dbID=0, classroomID=0)]
messages = [Message(contents="iamcontents", sentBy="iamname", sentByID=0, timeSent=0)]
bullying_requests = [BullyingRequest(requestedBy="iamname", requestedByID="iamid", cause="iamname", causeID="iamid", controlledBy="iamname", controlledByID="iamid", dbID=-1, completed=False)]

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

def update_student(password, studentClass, studentID):

    #The password and studentClass is what we want changed
    #We use studentID to find the student

    studentNeedingUpdate = BLANK_STUDENT

    for student in students:

        if (student.studentID == studentID):

            studentNeedingUpdate = student
        
    students[students.index(studentNeedingUpdate)] = Student(name=studentNeedingUpdate.name, password=password, studentClass=studentClass, studentID=studentNeedingUpdate.studentID, dbID=studentNeedingUpdate.dbID)

def delete_student(studentID):

    studentNeedingDeletion = BLANK_STUDENT

    for student in students:

        if (student.studentID == studentID):

            studentNeedingDeletion = student

    del students[students.index(studentNeedingDeletion):students.index(studentNeedingDeletion) + 1]

#Admin functions
def add_admin(name, password, controllingClass, role):

    admins.append(Admin(name=name, password=password, controllingClass=controllingClass, dbID=get_last_id(admins) + 1, role=role))

def get_admins():

    return admins

def get_admin_object_from_username_password(username, password, role):

    for admin in admins:

        if (admin.name == username and admin.password == password and admin.role == role):

            return admin
    
    return BLANK_ADMIN

def login_admin(username, password, role):

    return get_admin_object_from_username_password(username, password, role)

def update_admin(password, controllingClass, adminID):

    #The password and controllingClass is what we want changed
    #We use adminID to find the admin

    adminNeedingUpdate = BLANK_ADMIN

    for admin in admins:

        if (admin.adminID == adminID):

            adminNeedingUpdate = admin
        
    admins[admins.index(adminNeedingUpdate)] = Admin(name=adminNeedingUpdate.name, password=password, controllingClass=controllingClass, dbID=adminNeedingUpdate.dbID, adminID=adminID)

def delete_admin(adminID, role):

    adminNeedingDeletion = BLANK_ADMIN

    for admin in admins:

        if (admin.adminID == adminID):

            adminNeedingDeletion = admin

    del admins[admins.index(adminNeedingDeletion):admins.index(adminNeedingDeletion) + 1]

#Classroom Functions
def add_classroom(name, controllingTeacher):

    classrooms.append(Classroom(name=name, dbID=get_last_id(classrooms) + 1, controllingTeacher=controllingTeacher))

def get_classrooms():

    return classrooms

def get_classroom_object_from_name(name):

    for classroom in classrooms:

        if (classroom.name == name):

            return classroom
    
    return BLANK_CLASSROOM

def delete_classroom(name):

    for classroom in classrooms:

        if (classroom.name == name):

            classroomNeedingDeletion = classroom
    
    del classrooms[classrooms.index(classroomNeedingDeletion):classrooms.index(classroomNeedingDeletion) + 1]

#Message Functions
def add_message(contents, sentBy, sentByID, groupID):

    messages.append(Message(contents=contents, sentBy=sentBy, sentByID=sentByID, groupID=groupID, timeSent=int(time.time())))

def get_message():

    return admins

def get_message_from_time1_to_time2(time1, time2):

    messages_arr = []
    for i in messages:
        if i.timeSent >= time1 and i.timeSent <= time2:

            messages_arr.append(i)
            next(i)

    return messages_arr

#Group functions
def add_group(name, classroomID):

    classrooms.append(Group(name=name, dbID=get_last_id(groups) + 1, classroomID=classroomID))

def get_groups():

    return groups

def get_group_object_from_classroom_id(classroomID):

    for group in groups:

        if (group.classroomID == classroomID):

            return group
    
    return BLANK_GROUP

def delete_group(name, classroomID):

    for group in groups:

        if (group.name == name and group.classroomID == classroomID):

            groupNeedingDeletion = group
    
    del groups[groups.index(groupNeedingDeletion):groups.index(groupNeedingDeletion) + 1]

#Bullying request functions
def add_bullying_request(requestedBy, requestedByID, cause, causeID, controlledBy, controlledByID, completed):

    bullying_requests.append(BullyingRequest(requestedBy=requestedBy, requestedByID=requestedByID, cause=cause, causeID=causeID, controlledBy=controlledBy, controlledByID=controlledByID, dbID=get_last_id(bullying_requests) + 1, completed=completed))

def get_bullying_requests():

    return bullying_requests

def get_bullying_request_by_requestedID_and_causeID(requestedID, causeID):

    for request in bullying_requests:

        if (request.requestedByID == requestedID and request.causeID == causeID):

            return request
    
    return BLANK_BULLYING_REQUEST

def update_bullying_request(state, requestedID, causeID):

    bullying = get_bullying_request_by_requestedID_and_causeID(requestedID, causeID)
    bullying_requests[BullyingRequest.index(bullying)] = BullyingRequest(requestedBy=bullying.requestedBy, requestedByID=bullying.requestedByID, cause=bullying.cause, causeID=bullying.causeID, controlledBy=bullying.controlledBy, controlledByID=bullying.controlledByID, dbID=bullying.dbID, completed=state)