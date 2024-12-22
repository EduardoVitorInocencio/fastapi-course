from fastapi import Body, FastAPI

BOOKS = [
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'category': 'Fiction'},
    {'title': '1984', 'author': 'George Orwell', 'category': 'Dystopian'},
    {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'category': 'Romance'},
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'category': 'Classic'},
    {'title': 'Moby-Dick', 'author': 'Herman Melville', 'category': 'Adventure'},
    {'title': 'War and Peace', 'author': 'Leo Tolstoy', 'category': 'Historical Fiction'},
    {'title': 'One Hundred Years of Solitude', 'author': 'Gabriel García Márquez', 'category': 'Magical Realism'},
    {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'category': 'Literature'},
    {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'category': 'Fantasy'},
    {'title': 'Brave New World', 'author': 'Aldous Huxley', 'category': 'Dystopian'},
    
    {'title': 'Dom Casmurro', 'author': 'Machado de Assis', 'category': 'Brazilian Literature'},
    {'title': 'The Alchemist', 'author': 'Paulo Coelho', 'category': 'Adventure'},
    {'title': 'Memórias Póstumas de Brás Cubas', 'author': 'Machado de Assis', 'category': 'Classic'},
    {'title': 'A Moreninha', 'author': 'Joaquim Manuel de Macedo', 'category': 'Romance'},
    {'title': 'O Primo Basílio', 'author': 'José de Alencar', 'category': 'Novel'},
    {'title': 'O Guarani', 'author': 'José de Alencar', 'category': 'Historical Fiction'},
    {'title': 'Grande Sertão: Veredas', 'author': 'João Guimarães Rosa', 'category': 'Modernist'},
    {'title': 'O Cortiço', 'author': 'Aluisio Azevedo', 'category': 'Realism'},
    {'title': 'Iracema', 'author': 'José de Alencar', 'category': 'Romance'},
    {'title': 'Senhora', 'author': 'José de Alencar', 'category': 'Romance'},
    
    {'title': 'Le Petit Prince', 'author': 'Antoine de Saint-Exupéry', 'category': 'Children\'s Literature'},
    {'title': 'Les Misérables', 'author': 'Victor Hugo', 'category': 'Historical Fiction'},
    {'title': 'L\'Étranger', 'author': 'Albert Camus', 'category': 'Philosophical Fiction'},
    {'title': 'Le Comte de Monte-Cristo', 'author': 'Alexandre Dumas', 'category': 'Adventure'},
    {'title': 'Madame Bovary', 'author': 'Gustave Flaubert', 'category': 'Literary Fiction'},
    {'title': 'Les Fleurs du mal', 'author': 'Charles Baudelaire', 'category': 'Poetry'},
    {'title': 'Germinal', 'author': 'Émile Zola', 'category': 'Naturalism'},
    {'title': 'Le Rouge et le Noir', 'author': 'Stendhal', 'category': 'Historical Fiction'},
    {'title': 'La Peste', 'author': 'Albert Camus', 'category': 'Philosophical Fiction'},
    {'title': 'L’Assommoir', 'author': 'Émile Zola', 'category': 'Naturalism'},
    
    {'title': 'Cien años de soledad', 'author': 'Gabriel García Márquez', 'category': 'Magical Realism'},
    {'title': 'Don Quijote de la Mancha', 'author': 'Miguel de Cervantes', 'category': 'Classic'},
    {'title': 'Ficciones', 'author': 'Jorge Luis Borges', 'category': 'Short Stories'},
    {'title': 'El amor en los tiempos del cólera', 'author': 'Gabriel García Márquez', 'category': 'Romance'},
    {'title': 'La sombra del viento', 'author': 'Carlos Ruiz Zafón', 'category': 'Mystery'},
    {'title': 'Rayuela', 'author': 'Julio Cortázar', 'category': 'Modernist'},
    {'title': 'El túnel', 'author': 'Ernesto Sabato', 'category': 'Psychological Fiction'},
    {'title': 'Pedro Páramo', 'author': 'Juan Rulfo', 'category': 'Magical Realism'},
    {'title': 'Cumbres Borrascosas', 'author': 'Emily Brontë', 'category': 'Gothic'},
    {'title': 'Fahrenheit 451', 'author': 'Ray Bradbury', 'category': 'Dystopian'},
    
    {'title': 'The Shining', 'author': 'Stephen King', 'category': 'Horror'},
    {'title': 'A Brief History of Time', 'author': 'Stephen Hawking', 'category': 'Science'},
    {'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'category': 'Mystery'},
    {'title': 'The Girl with the Dragon Tattoo', 'author': 'Stieg Larsson', 'category': 'Thriller'},
    {'title': 'The Road', 'author': 'Cormac McCarthy', 'category': 'Post-apocalyptic'},
    {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'category': 'Fantasy'},
    {'title': 'The Hunger Games', 'author': 'Suzanne Collins', 'category': 'Dystopian'},
    {'title': 'Harry Potter and the Sorcerer\'s Stone', 'author': 'J.K. Rowling', 'category': 'Fantasy'},
    {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'category': 'Literature'},
    {'title': 'The Help', 'author': 'Kathryn Stockett', 'category': 'Historical Fiction'}
]

app = FastAPI()
# ------------------------------------------------------------------------------
@app.get("/api-endpoint")
async def first_api():
    return BOOKS

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold()==book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold()==category.casefold():
            books_to_return.append(book)

    return books_to_return

@app.get("/books/byauthor/")
async def read_books_by_author_query(author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    
    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold()==book_author.casefold() and book.get('category').casefold()==category.casefold():
            books_to_return.append(book)

    return books_to_return

# CADASTRAR
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book

# ATUALIZAR
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold()==updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return updated_book

###################################################################################

# FASTAPI Assignment

# 1. Create a new API Endpoint that can fetch 
# all books from a specific author using either 
# Path Parameters or Query Parameters.

@app.get("/books/author/{book_author}")
async def read_books_by_author_path(book_author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold()==book_author.casefold():
            books_to_return.append(book)
    
    return books_to_return

###################################################################################


