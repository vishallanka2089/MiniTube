from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# Database connection
try:
    DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
    #print(DATABASE_URL)
    engine = create_engine(DATABASE_URL)
    print("DataBase Connected!")
except Exception as e:
    print(f"An error occurred: {e}")

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependency for ORM
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastAPI',user='postgres',password='Vsc@A203',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connected!")
#         break
#     except Exception as error:
#         print("Connection Failed!")
#         print(f"The Error is: {error}")
#         time.sleep(3)
