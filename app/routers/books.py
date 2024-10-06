from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.models import Book
from app.schemas import BookCreate, BookUpdate
from app.dependencies import db_dependency

router = APIRouter()

@router.post("/add-book")
def create_book(book: BookCreate, session: Session = db_dependency):
    statement = select(Book).where(Book.title == book.title)
    existing_book = session.exec(statement).first()

    if existing_book:
        raise HTTPException(status_code=400, detail="A book with this title already exists")
    db_book = Book(
        title=book.title, 
        publication_year=book.publication_year, 
        author_id=book.author_id
        )
    
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.get("/fetch-books")
def fetch_books(session: Session = db_dependency):
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

# update book route
@router.put("/update-book/{book_id}")
def update_book(book_id: int, book: BookUpdate, session: Session = db_dependency):
    statement = select(Book).where(Book.id == book_id)
    existing_book = session.exec(statement).first()
    print(existing_book.author)

    if not existing_book:
        raise HTTPException(status_code=400, detail="book not found")
    
    book_data = book.dict(exclude_unset=True)

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
