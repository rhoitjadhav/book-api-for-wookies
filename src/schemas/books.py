# Packages
from typing import Optional
from pydantic import BaseModel


class BooksAddSchema(BaseModel):
    title: str
    description: str
    cover_image: str
    price: int
    author: str


class BooksUpdateSchema(BaseModel):
    title: str
    description: str
    cover_image: str
    price: int
