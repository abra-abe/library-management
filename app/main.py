from fastapi import FastAPI
from app.routers import authors, books
from app.db import init_db

app = FastAPI()

# initialize the db
init_db()

# including the routes
app.include_router(authors.router)
app.include_router(books.router)

# root route
@app.get("/")
def home():
    return{"message": "this is the home route"}