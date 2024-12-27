from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published: int

    def __init__(self, id, title, author, description, rating, published):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published = published

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed o create', default=None)
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=1, max_length=50)
    description:str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=1, lt=5)
    published: Optional[int] = Field(gt=1900, lt=2025, default=None)

    model_config = {
        "json_schema_extra":{
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A story about the American Dream",
                "rating": 5,
                "published":2000
            }
        }
    }

BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "A story about the American Dream", 5, 2020),
    Book(2, "The Da Vinci Code", "Dan Brown ", "A story about the American Dream", 4, 2014),
    Book(3, "The Catcher in the Rye", "J.D. Salinger", "A story about the American Dream", 3, 2007),
    Book(4, "The Hunger Games", "Suzanne Collins", "A story about the American Dream", 2,2024),
    Book(5, "The Help", "Kathryn Stockett", "A story about the American Dream", 1, 2023),
    Book(6, "The Road", "Cormac McCarthy", "A story about the American Dream", 5, 2023),
    Book(7, "The Lord of the Rings", "J.R.R. Tolkien", "A story about the American Dream", 4, 1999)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_year(publish_year: int = Query(gt=1900, lt=2025)):
    books_to_return = []
    for book in BOOKS:
        if book.published == publish_year:
            books_to_return.append(book)

    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    raise HTTPException(status_code=404, detail="Book not found")


def find_book_id(book: Book):

    book.id=1 if len(BOOKS)== 0 else BOOKS[-1].id+1
    return book


@app.post("/books/create_book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
    raise HTTPException(status_code=404, detail="Book not found")   


 



