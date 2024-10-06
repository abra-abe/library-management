from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.models import Author
from app.schemas import AuthorCreate
from app.dependencies import db_dependency

router = APIRouter()

@router.post("/add-author")
def create_authors(author: AuthorCreate, session: Session = db_dependency):
    db_author = Author(name = author.name)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author