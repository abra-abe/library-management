from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str

class BookCreate(BaseModel):
    title: str
    plublication_year: int
    author_id: int

class BookUpdate(BaseModel):
    title: Optional[str]
    publication_year: Optional[int]
    author_id: Optional[int]
