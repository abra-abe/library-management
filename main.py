from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

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

app = FastAPI()

@app.get("/")
def home():
    return {"message": "welcome to the home directory"}