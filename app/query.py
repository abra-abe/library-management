from sqlmodel import Session, select

from app.models import Book
from app.schemas import BookCreate


class BookQuery:

    def __init__(self,session:Session):
        self.session=session
    def save(self,book:BookCreate):
        with self.session:
            db_book = Book(
        title=book.title, 
        publication_year=book.publication_year, 
        author_id=book.author_id
        )
    
            self.session.add(db_book)
            self.session.commit()
            self.session.refresh(db_book)

            return db_book
        pass

    def get_by_title(self,title:str):
        with self.session:
            statement = select(Book).where(Book.title == title)
            return self.session.exec(statement).first()

