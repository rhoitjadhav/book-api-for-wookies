# Packages
import unittest
from unittest.mock import patch
from mock_alchemy.mocking import AlchemyMagicMock


# Modules
from models.books import BooksModel
from usecases.books import BooksUsecase
from schemas.books import BooksAddSchema, BooksUpdateSchema


class TestBooks(unittest.TestCase):
    _books_usecase = BooksUsecase()

    def setUp(self) -> None:
        self._db = AlchemyMagicMock()

    def test_get_book_by_id_response_status(self):
        self._db.query(BooksModel).filter(
            BooksModel.id == 1).first.return_value = BooksModel
        response = self._books_usecase.get_book_by_id(self._db, 1, BooksModel)
        self.assertTrue(response.status)

    def test_get_list_books_empty_response(self):
        self._db.query(BooksModel).offset(0).limit(10).all.return_value = []
        response = self._books_usecase.list_books(self._db, 1, BooksModel)
        self.assertEqual([], response.data)

    def test_get_list_books_single_response(self):
        self._db.query(BooksModel).offset(0).limit(10).all.return_value = {
            "description": "Influence People",
            "title": "How to win Friends",
            "price": 200,
            "cover_image": "AIJ3P9_requirements.txt",
            "id": 1,
            "author": "Mikal"
        }
        response = self._books_usecase.list_books(self._db, 1, BooksModel)
        self.assertEqual("Mikal", response.data["author"])

    def test_get_list_books_by_title(self):
        author = "some-author"
        book = BooksModel(**{
            "description": "Influence People",
            "title": "How to win Friends",
            "price": 200,
            "cover_image": "AIJ3P9_requirements.txt",
            "id": 1,
            "author": "some-author"
        })
        self._db.query(BooksModel).filter(
            BooksModel.author.like(f"%{author}%")).limit(10).all.return_value = [book]

        response = self._books_usecase.list_books_by_search_query(
            self._db, BooksModel, author=author)
        self.assertEqual("some-author", list(response.data)[0].author)

    @patch.object(BooksUsecase, "_is_book_cover_image_exists", return_value=True)
    def test_create_book_response_status(self, mock_image_exists):
        book = {
            "title": "How to win Friends",
            "description": "Influence People",
            "cover_image": "AIJ3P9_requirements.txt",
            "price": "200",
            "author": "Mikal"
        }
        book_schema = BooksAddSchema(**book)
        response = self._books_usecase.create_book(
            self._db, book_schema, book_schema.author, BooksModel,
        )
        self.assertTrue(response.status)

    @patch.object(BooksUsecase, "_is_book_cover_image_exists", return_value=True)
    def test_create_book_response_data(self, mock_image_exists):
        book = {
            "title": "How to win Friends",
            "description": "Influence People",
            "cover_image": "AIJ3P9_requirements.txt",
            "price": "200",
            "author": "Mikal"
        }
        book_schema = BooksAddSchema(**book)
        response = self._books_usecase.create_book(
            self._db, book_schema, book_schema.author, BooksModel
        )
        self.assertEqual(200, response.data.price)

    @patch.object(BooksUsecase, "_is_book_cover_image_exists", return_value=True)
    def test_create_book_with_user_Darth_Vader(self, mock_image_exists):
        book = {
            "title": "How to win Friends",
            "description": "Influence People",
            "cover_image": "cover_image_test.txt",
            "price": 201,
            "author": "Darth Vader"
        }
        book_schema = BooksAddSchema(**book)
        response = self._books_usecase.create_book(
            self._db, book_schema, book_schema.author, BooksModel
        )
        self.assertEqual(403, response.http_code)

    def test_delete_book_and_check_book_not_exists_in_response_message(self):
        self._db.query(BooksModel).filter(BooksModel.id ==
                                          1).first.return_value = None
        response = self._books_usecase.delete_book(
            self._db, 1, "Mikal", BooksModel)
        self.assertEqual("Book not exists", response.message)

    def test_update_book_and_check_response_data(self):
        book = {
            "title": "How to win Friends",
            "description": "Influence People",
            "cover_image": "cover_image_test.txt",
            "price": 201,
        }
        book_schema = BooksUpdateSchema(**book)
        self._db.query(BooksModel).filter(
            BooksModel.id == 1).first.return_value = BooksModel(**book, author="rohit123")

        response = self._books_usecase.update_book(
            self._db, 1, "rohit123", book_schema, BooksModel,
        )
        self.assertEqual(201, response.data.price)
