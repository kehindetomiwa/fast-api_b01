from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status


from pydantic import BaseModel, Field


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author =  author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on created', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2023)

    # used to configure swagger
    # set example post at swagger load
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "a new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029
            }
        }
    }




BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 3, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

# get all books
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

# use Path from fast API to validate path parameter
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_a_book(book_id: int = Path(gt=0)):
    print("------>  ", type(book_id))
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Item with id:{book_id} not found")

@app.get("/books/published_date/{published_date}", status_code=status.HTTP_200_OK)
async def read_book_by_rating(published_date: int = Path(gt=1999, lt=2031)):
    book_to_rate = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_to_rate.append(book)
    return book_to_rate

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(ge=1, le=5)):
    book_to_rate = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_rate.append(book)
    return book_to_rate


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async  def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail=f"Item with id {book.id} not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
    if not book_change:
        raise HTTPException(status_code=404, detail=f"Item with id {book_id} not found")

