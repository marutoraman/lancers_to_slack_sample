from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session,Session
import os
import ulid
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get("DB_CONNECTION_PATH")
if SQLALCHEMY_DATABASE_URL == None:
  raise Exception("db connection error")
SQLALCHEMY_DATABASE_URL += '?charset=utf8mb4'
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=360,pool_size=100)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(bind=engine)
session = scoped_session(SessionLocal)


# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close() # pylint: disable=no-member

def get_db_instance():
  return SessionLocal()

def get_ulid():
  return ulid.new().str

