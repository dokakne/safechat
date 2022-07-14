from calendar import EPOCH
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
    timeSent: EPOCH

class BullyingRequest(BaseModel):

    requestedBy: str
    requestedByID: str
    cause: str
    causeID: str
    controlledBy: str
    controlledByID: str
    dbID: int
    completed: bool

'''class Teacher(BaseModel):

    name: str
    password: str
    teacherID: int
    dbID: int
    controllingClass: str

class Counsellor(BaseModel):

    name: str
    password: str
    dbID: int
    counsellorID: int
    responsibleClass: str'''

BLANK_STUDENT = Student(name="", password="", studentClass="", studentID=-1, dbID=-1)
BLANK_ADMIN = Admin(name="", password="", controllingClass="", dbID=-1, adminID=-1, role="")
# BLANK_TEACHER = Teacher(name="", password="", studentID=-1, dbID=0, controllingClass="")
# BLANK_COUNSELLOR = Counsellor(name="", password="", dbID=-1, counsellorID=0, responsibleClass="")
BLANK_CLASSROOM = Classroom(name="", dbID=-1, controllingTeacher="")
BLANK_GROUP = Group(name="", dbID=-1, classroomID=-1)
BLANK_MESSAGE = Message(contents="", sentBy="", sentByID=-1, timeSent=0)
BLANK_BULLYING_REQUEST = BullyingRequest(requestedBy="", requestedByID="", cause="", causeID="", controlledBy="", controlledByID="", dbID=-1, completed=False)

students = [Student(name="iamname", password="iampassword", studentClass="nope", studentID=0, dbID=0)]
admins = [Admin(name="iamname", password="iampassword", controllingClass="Nope", dbID=0, adminID="admin-1", role="Nope")]
# teachers = [Teacher(name="iamname", password="iampassword", studentID=0, dbID=0, controllingClass="")]
# counsellors = [Counsellor(name="iamname", password="iampassword", dbID=0, counsellorID=0, responsibleClass="")]
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

'''
#Teacher functions
def add_teacher(name, password, teacherID, controllingClass):

    teachers.append[Teacher(name=name, password=password, teacherID=teacherID, dbID=get_last_id(teachers) + 1, controllingClass=controllingClass)]

def get_teachers():

    return teachers

def get_teacher_object_from_username_password(username, password):

    for teacher in teachers:

        if (teacher.name == username and teacher.password == password):

            return teacher
    
    return BLANK_TEACHER

def login_teacher(username, password):

    return get_teacher_object_from_username_password(username, password)

def update_teacher(password, controllingClass, teacherID):

    #The password and controllingClass is what we want changed
    #We use teacherID to find the teacher

    teacherNeedingUpdate = BLANK_ADMIN

    for teacher in teachers:

        if (teacher.teacherID == teacherID):

            teacherNeedingUpdate = teacher
        
    teachers[teachers.index(teacherNeedingUpdate)] = Teacher(name=teacherNeedingUpdate.name, password=password, teacherID=teacherID, dbID=get_last_id(teachers) + 1, controllingClass=controllingClass)

def delete_teacher(teacherID):

    teacherNeedingDeletion = BLANK_ADMIN

    for teacher in teachers:

        if (teacher.teacherID == teacherID):

            teacherNeedingDeletion = teacher

    del teachers[teachers.index(teacherNeedingDeletion):teachers.index(teacherNeedingDeletion) + 1]

#Counsellor functions
def add_counsellor(name, password, counsellorID, controllingClass):

    counsellors.append[Counsellor(name=name, password=password, dbID=get_last_id(counsellors) + 1, counsellorID=counsellorID, controllingClass=controllingClass)]

def get_counsellors():

    return counsellors

def gte_counsellors_from_username_password(username, password):

    for counsellor in counsellors:

        if (counsellor.name == username and counsellor.password == password):

            return counsellor
    
    return BLANK_COUNSELLOR

def login_counsellor(username, password):

    return gte_counsellors_from_username_password(username, password)

def update_counsellor(password, responsibleClass, counsellorID):

    counsellorNeedingUpdate = BLANK_COUNSELLOR

    for counsellor in counsellors:

        if (counsellor.counsellorID== counsellorID):

            counsellorNeedingUpdate = counsellor
        
    counsellors[counsellors.index(counsellorNeedingUpdate)] = Counsellor(name=counsellorNeedingUpdate.name, password=password, dbID=counsellorNeedingUpdate.dbID, counsellorID=counsellorID, responsibleClass=responsibleClass) 

def delete_counsellor(counsellorID):

    counsellorNeedingDeletion = BLANK_COUNSELLOR

    for counsellor in counsellors:

        if (counsellor.counsellorID == counsellorID):

            counsellorNeedingDeletion = counsellor

    del counsellors[counsellors.index(counsellorNeedingDeletion):counsellors.index(counsellorNeedingDeletion) + 1]
    '''