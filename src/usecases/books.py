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
    FORBIDDEN_USERS
)


class BooksUsecase:
    @staticmethod
    def _is_book_cover_image_exists(cover_image: str) -> bool:
        """Check if book cover image file exists in local storage

        Args:
            cover_image: name of cover image

        Returns:
            True if cover image file exists otherwise False
        """
        file_path = os.path.join(STATIC_FILES_PATH, cover_image)
        return os.path.exists(file_path)

    @staticmethod
    def _is_user_forbidden_from_creating_book(
        author_pseudonym: str
    ) -> bool:
        """Check if the author is forbidden to create/publish the books

        Args:
            author_pseudonym: name of author

        Returns:
            True if author is forbidden otherwise False
        """
        return True if author_pseudonym in FORBIDDEN_USERS else False

    @staticmethod
    def create_book(
        db: Session,
        book_schema: BooksAddSchema,
        author_pseudonym: str,
        book_model: Type[BooksModel]
    ) -> ReturnValue:
        """Create book

        Args:
            db: sqlalchemy instance
            book_schema: book payload in schema format
            author_pseudonym: author of the book
            book_model: BooksModel instance

        Returns:
            True if book created otherwise False
        """
        if not author_pseudonym == book_schema.author:
            return ReturnValue(False, status.HTTP_401_UNAUTHORIZED, "Author name mismatched")

        if BooksUsecase._is_user_forbidden_from_creating_book(author_pseudonym):
            return ReturnValue(False, status.HTTP_403_FORBIDDEN, "Forbidden access: Not allowed to publish books")

        if not BooksUsecase._is_book_cover_image_exists(book_schema.cover_image):
            return ReturnValue(
                False,
                status.HTTP_404_NOT_FOUND,
                "Cover image doesn't exists, please upload first"
            )

        book = book_model(**book_schema.dict())
        db.add(book)
        db.commit()
        db.refresh(book)
        return ReturnValue(True, status.HTTP_200_OK, "Book Added", data=book)

    @staticmethod
    def get_book_by_id(
        db: Session,
        book_id: int,
        book_model: Type[BooksModel]
    ) -> ReturnValue:
        """Get book details by book_id

        Args:
            db: sqlalchemy instance_
            book_id: id of book
            book_model: BooksModel instance

        Returns:
            return books details if exists otherwise False
        """
        book = db.query(book_model).filter(book_model.id == book_id).first()
        if not book:
            return ReturnValue(False, status.HTTP_404_NOT_FOUND, "Book not exists")

        return ReturnValue(True, status.HTTP_200_OK, message="Book found", data=book)

    @staticmethod
    def list_books(
        db: Session,
        book_model: Type[BooksModel],
        limit: int = 10,
        skip: int = 0
    ) -> ReturnValue:
        """List/Details of Books

        Args:
            db: sqlalchemy instance
            book_model: BooksModel instance
            limit: number of rows to be fetched from database. Defaults to 10.
            skip: number of rows to be skipped. Defaults to 0.

        Returns:
            list of books
        """
        books = db.query(book_model).offset(skip).limit(limit).all()
        return ReturnValue(True, status.HTTP_200_OK, message="Books Fetched", data=books)

    @staticmethod
    def list_books_by_search_query(
        db: Session,
        book_model: Type[BooksModel],
        title: str = None,
        description: str = None,
        author: str = None,
        limit: int = 10,
    ) -> ReturnValue:
        """List books using search query

        Args:
            db: sqlalchemy instance
            book_model: BooksModel instance
            title: title of book. Defaults to None.
            description: descriptio of book. Defaults to None.
            author: author of book. Defaults to None.
            limit: number of rows to be fetched from database. Defaults to 10.

        Returns:
            list of books based on search query
        """
        books = []
        if title:
            books_with_title = db.query(book_model).filter(
                book_model.title.like(f"%{title}%")).limit(limit).all()
            books.extend(books_with_title)

        if description:
            books_with_description = db.query(book_model).filter(
                book_model.description.like(f"%{description}%")).limit(limit).all()
            books.extend(books_with_description)

        if author:
            books_with_author = db.query(book_model).filter(
                book_model.author.like(f"%{author}%")).limit(limit).all()
            books.extend(books_with_author)

        return ReturnValue(True, status.HTTP_200_OK, message="Books Fetched", data=set(books))

    @staticmethod
    def update_book(
        db: Session,
        book_id: int,
        author_pseudonym: str,
        book_schema: BooksUpdateSchema,
        book_model: Type[BooksModel]
    ) -> ReturnValue:
        """Update book record

        Args:
            db: sqlalchemy instance
            book_id: book id
            author_pseudonym: author of the book
            book_schema: book payload in schema format
            book_model: BooksModel instance

        Returns:
            True if book is updated otherwise False
        """
        book = db.query(book_model).filter(book_model.id == book_id).first()
        if not book:
            return ReturnValue(False, status.HTTP_404_NOT_FOUND, "Book not exists")

        if not author_pseudonym == book.author:
            return ReturnValue(False, status.HTTP_401_UNAUTHORIZED, "Unauthorized operation")

        if not BooksUsecase._is_book_cover_image_exists(book_schema.cover_image):
            return ReturnValue(
                False,
                status.HTTP_404_NOT_FOUND,
                "Cover image doesn't exists, please upload first"
            )

        book.title = book_schema.title
        book.description = book_schema.description
        book.cover_image = book_schema.cover_image
        book.price = book_schema.price
        db.commit()

        return ReturnValue(True, status.HTTP_200_OK, "Book details updated", data=book_schema)

    @staticmethod
    def delete_book(
        db: Session,
        book_id: int,
        author_pseudonym: str,
        book_model: Type[BooksModel]
    ) -> ReturnValue:
        """Delete book record

        Args:
            db: sqlalchemy instance
            book_id: book id
            author_pseudonym: author of the book
            book_model: BooksModel instance

        Returns:
            True if book is deleted otherwise False
        """
        book = db.query(book_model).filter(book_model.id == book_id).first()
        if not book:
            return ReturnValue(False, status.HTTP_404_NOT_FOUND, "Book not exists")

        if not author_pseudonym == book.author:
            return ReturnValue(False, status.HTTP_401_UNAUTHORIZED, "Unauthorized operation")

        db.delete(book)
        db.commit()
        return ReturnValue(True, status.HTTP_200_OK, "Book Deleted", data=book)

    @staticmethod
    def upload_cover_image(file: UploadFile) -> ReturnValue:
        """Upload cover image file

        Args:
            file: UploadFile object

        Returns:
            True if file is saved
        """
        filename = f"{Helper.generate_random_text()}_{file.filename}"
        file_path = os.path.join(STATIC_FILES_PATH, filename)
        with open(file_path, "wb+") as fb:
            fb.write(file.file.read())

        return ReturnValue(True, status.HTTP_200_OK, "File Saved", data=filename)
