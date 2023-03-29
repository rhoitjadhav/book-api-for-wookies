# Packages
import os
from typing import Type
from sqlalchemy.orm import Session
from fastapi import status, UploadFile

# Modules
from models.books import BooksModel
from utils.helper import ReturnValue, Helper
from schemas.books import BooksAddSchema, BooksUpdateSchema
from config import (
    AUTH_SECRET_KEY,
    AUTH_ALGORITHM,
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES,
    STATIC_FILES_PATH,
)


class BooksUsecase:
    @staticmethod
    def _is_book_cover_image_exists(cover_image: str):
        print(cover_image)
        file_path = os.path.join(STATIC_FILES_PATH, cover_image)
        return os.path.exists(file_path)

    @staticmethod
    def create_book(db: Session, book_schema: BooksAddSchema, book_model: Type[BooksModel]):
        if not BooksUsecase._is_book_cover_image_exists(book_schema.cover_image):
            return ReturnValue(False, status.HTTP_404_NOT_FOUND, "Cover image doesn't exists, please upload first")

        book = book_model(**book_schema.dict())
        db.add(book)
        db.commit()
        db.refresh(book)
        return ReturnValue(True, status.HTTP_200_OK, "Book Added", data=book)

    @staticmethod
    def get_book_by_id(db: Session, book_id: int, book_model: Type[BooksModel]):
        book = db.query(book_model).filter(book_model.id == book_id).first()
        if not book:
            return ReturnValue(False, status.HTTP_404_NOT_FOUND, "Book not exists")

        return ReturnValue(True, status.HTTP_200_OK, message="Book found", data=book)

    @staticmethod
    def list_books(db: Session, book_model: Type[BooksModel], limit: int = 10, skip: int = 0):
        books = db.query(book_model).offset(skip).limit(limit).all()
        return ReturnValue(True, status.HTTP_200_OK, message="Books Fetched", data=books)

    @staticmethod
    def update_book(db: Session, book_id: int, book_schema: BooksUpdateSchema, book_model: Type[BooksModel]):
        db.query(book_model).filter(book_model.id ==
                                    book_id).update(book_schema.dict())
        db.commit()
        return ReturnValue(True, status.HTTP_200_OK, "Book details updated", data=book_schema)

    @staticmethod
    def delete_book(db: Session, book_id: int, book_model: Type[BooksModel]):
        result = BooksUsecase.get_book_by_id(db, book_id, book_model)
        if not result.status:
            return result
        book = db.query(book_model).filter(book_model.id == book_id).first()
        db.delete(book)
        db.commit()
        return ReturnValue(True, status.HTTP_200_OK, "Book Deleted", data=book)

    @staticmethod
    def upload_cover_image(file: UploadFile):
        filename = f"{Helper.generate_random_text()}_{file.filename}"
        file_path = os.path.join(STATIC_FILES_PATH, filename)
        with open(file_path, "wb+") as fb:
            fb.write(file.file.read())

        return ReturnValue(True, status.HTTP_200_OK, "File Saved", data=filename)
