from jose import jwt, JWTError
import os
from passlib.context import CryptContext

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):

    return pwd_context.hash(password)

print(pwd_context.verify("123", hash_password("123")))