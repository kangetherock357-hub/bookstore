from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select, Session, SQLModel
from models.book import Book, BookCreate, BookUpdate
from database.session import get_session, engine


app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/books", response_model=Book)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    db_book = Book.from_orm(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books", response_model=list[Book])
def list_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book_update.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(book, key, value)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}

@app.get("/books/search", response_model=list[Book])
def search_books(query: str, session: Session = Depends(get_session)):
    statement = select(Book).where(
        (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
    )
    return session.exec(statement).all()
