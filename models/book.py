from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class BookBase(SQLModel):
    title: str = Field(index=True, nullable=False)
    author: str = Field(index=True, nullable=False)
    isbn: str = Field(index=True, unique=True, nullable=False)
    published_year: int = Field(ge=1000, le=datetime.now().year)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    available: bool = Field(default=True)

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BookCreate(BookBase):
    pass

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    available: Optional[bool] = None
