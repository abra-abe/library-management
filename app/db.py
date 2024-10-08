from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session