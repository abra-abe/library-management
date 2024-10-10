from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str

class BookCreate(BaseModel):
    title: str
    publication_year: int
    author_id: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    publication_year: Optional[int] = None
    author_id: Optional[int] = None

class Author(BaseModel):
    id: int
    name: str

class BookResponse(BaseModel):
    id:int
    title: str
    publication_year: int
    author: Author

