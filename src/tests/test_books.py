# Packages
import unittest
from unittest.mock import MagicMock, patch


# Modules
from usecases.books import BooksUsecase


class TestBooks(unittest.TestCase):
    _books_usecase = BooksUsecase()

    def test_get_book_by_id():
        pass

    def test_create_book():
        pass

    def test_update_book():
        pass

    def test_delete_book():
        pass

    def test_upload_cover_image():
        pass
