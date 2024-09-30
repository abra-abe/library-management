from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Annotated
from sqlmodel import Session, select
from db import get_session, init_db
from models import Author, Book

app = FastAPI()

# initialize db
init_db()

# pydantic models
class AuthorCreate(BaseModel):
    name: str

class BookCreate(BaseModel):
    title: str
    publication_year: int
    author_id: int

class BookUpdate(BaseModel):
    title: Optional[str]
    publication_year: Optional[int]
    author_id: Optional[int]

db_dependency = Annotated[Session, Depends(get_session)]

@app.get("/")
def home():
    return {"message": "welcome to the home directory"}

# create authors route
@app.post("/add-author")
def create_authors(author: AuthorCreate, session: db_dependency):
    db_author = Author(name = author.name)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

# create book route
@app.post("/add-book")
def create_book(book: BookCreate, session: db_dependency):
    db_book = Book(title=book.title, publication_year=book.publication_year, author_id=book.author_id)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# get books route
@app.get("/fetch-books")
def fetch_books(session: db_dependency):
    statement = select(Book)
    books = session.exec(statement).all()
    return [
        {
            "title": book.title,
            "publication_year": book.publication_year,
            "author": {
                "id": book.author_id,
                "name": book.author.name
            }
        }
        for book in books
    ]