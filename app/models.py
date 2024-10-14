from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# for authors
class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    nationality: str
    books: List["Book"] = Relationship(back_populates="author")

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    publication_year: int
    author_id: int = Field(foreign_key="author.id")
    author: Optional[Author] = Relationship(back_populates="books")

    def save(self):
        pass