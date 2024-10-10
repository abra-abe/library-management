from typing import List

from fastapi import APIRouter, HTTPException,status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.dependencies import db_dependency
from app.models import Book
from app.query import BookQuery
from app.schemas import BookCreate, BookResponse, BookUpdate

router = APIRouter(tags=["Books"])

@router.post("/book")
def create_book(book: BookCreate, session: Session = db_dependency):
    existing_book = BookQuery(session).get_by_title(title=book.title)

    if existing_book:
        # raise HTTPException(status_code=400, detail="A book with this title already exists")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=f"A book with the title {book.title}, already exists")
    return BookQuery(session).save(book)

@router.get("/books",response_model=List[BookResponse])
def fetch_books(session: Session = db_dependency):
    statement = select(Book)
    books = session.exec(statement).all()
    return [
        {
            "id":book.id,
            "title": book.title,
            "publication_year": book.publication_year,
            "author": {
                "id": book.author_id,
                "name": book.author.name
            }
        }
        for book in books
    ]

# update book route
@router.put("/book/{book_id}")
def update_book(book_id: int, book: BookUpdate, session: Session = db_dependency):
    statement = select(Book).where(Book.id == book_id)
    existing_book = session.exec(statement).first()

    if not existing_book:
        # raise (status_code=400, detail="book not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="Book not found")
    
    book_data = book.dict(exclude_unset=True, exclude_none=True)

    for key, value in book_data.items():
        setattr(existing_book, key, value)
    
    # if book.title is not None:
    #     existing_book.title = book.title

    # if book.publication_year is not None:
    #     existing_book.publication_year = book.publication_year

    # if book.author_id is not None:
    #     existing_book.author_id = book.author_id

    # Commit the changes to the database
    session.add(existing_book)
    session.commit()
    session.refresh(existing_book)

    # Return the updated book
    return existing_book
