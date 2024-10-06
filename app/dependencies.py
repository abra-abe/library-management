# from sqlmodel import Session
from fastapi import Depends
from app.db import get_session

db_dependency = Depends(get_session)