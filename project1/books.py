from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException, Body
from starlette import status

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

# get books by title using a dynamic parameter
@app.get("/books/{book_title}", status_code=status.HTTP_200_OK)
async def read_all_books_dy(book_title: str):
    for book in BOOKS:
        if book.title.casefold() == book_title.casefold():
            return book

# dynamic parameter 2
@app.get("/bookss/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

# get books using query parameter
@app.get("/books/author/", status_code=status.HTTP_200_OK)
async def read_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        print(book.author.casefold(), author.casefold())
        if book.author.casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

# dynamic param and query param
@app.get("/books/{author}/", status_code=status.HTTP_200_OK)
async def read_by_author(author: str, rating: int):
    books_to_return = []
    for book in BOOKS:
        print(book.author.casefold(), author.casefold())
        if book.author.casefold() == author.casefold() and book.rating == rating:
            books_to_return.append(book)
    return books_to_return



BOOKS2 = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS2.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS2)):
        if BOOKS2[i].get('title').casefold() == updated_book.get("title").casefold():
            BOOKS2[i] = updated_book

@app.delete("/books/delete/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break