# #Used for utility functions like hashing

# from passlib.context import CryptContext #pip install "passlib[bcrypt]"
# pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

# def hash(password:str):
#     return pwd_context.hash(password)

# def verify(plain_password,hashed_password):
#     return pwd_context.verify(plain_password,hashed_password)

import bcrypt

def hash(password: str):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify(plain_password: str, hashed_password: str):
    """Verify a password against a bcrypt hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))