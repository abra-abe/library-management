from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.dependencies import db_dependency
from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate

router = APIRouter(tags=["Authors"])

@router.post("/author")
def create_author(author: AuthorCreate, session: Session = db_dependency):
    db_author = Author(name = author.name, nationality=author.nationality)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@router.put("/author/{author_id}")
def update_author(author_id: int, author: AuthorUpdate, session: Session = db_dependency):
    statement = select(Author).where(Author.id == author_id)
    existing_author = session.exec(statement).first()

    if not existing_author:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"no author with id {author_id}")
    
    author_data = author.dict(exclude_unset=True, exclude_none=True)

    for key, value in author_data.items():
        setattr(existing_author, key, value)
    
    session.add(existing_author)
    session.commit()
    session.refresh(existing_author)

    return existing_author