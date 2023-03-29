# Packages
import unittest
from unittest.mock import MagicMock, patch
from mock_alchemy.mocking import AlchemyMagicMock


# Modules
from utils.helper import Helper
from models.users import UsersModel
from usecases.users import UsersUsecase
from schemas.users import UsersSignUpSchema, UsersSignInSchema


class TestUsers(unittest.TestCase):
    _users_usecase = UsersUsecase()

    def setUp(self) -> None:
        self._db = AlchemyMagicMock()

    @patch.object(UsersUsecase, "_is_username_exists", return_value=False)
    @patch.object(UsersUsecase, "_is_email_exists", return_value=False)
    def test_user_sign_up_response_status(self, mock_username_exists, mock_email_exists):
        user = {
            "first_name": "rohit",
            "last_name": "jadhav",
            "email": "rohit@gmail.com",
            "username": "rohit",
            "password": "1234",
            "author_pseudonym": "rohit123"
        }
        user_schema = UsersSignUpSchema(**user)

        response = self._users_usecase.sign_up(
            self._db, user_schema, UsersModel
        )
        self.assertTrue(response.status)

    @patch.object(Helper, "create_access_token", return_value="")
    def test_user_sign_in_with_correct_credentials(self, mock_create_access):
        user_schema = UsersSignInSchema(
            **{"username": "rohit", "password": "1234"})
        user = MagicMock()
        user.username = "rohit"
        user.password = "$2b$12$j.hvS0zGfKRSvKPYdBSeruN5SWQVfTkMnpR.eRHRVLb.dxq2UmOOG"
        self._db.query(UsersModel).filter(
            UsersModel.username == user_schema.username).first.return_value = user

        response = self._users_usecase.sign_in(
            self._db, user_schema, UsersModel
        )
        self.assertTrue(response.status)

    def test_user_sign_in_with_incorrect_credentials(self):
        user_schema = UsersSignInSchema(
            **{"username": "rohit", "password": "wrong-password"})
        user = MagicMock()
        user.sub = "rohit"
        user.email = "rohit@gmail.com"
        user.username = "rohit"
        user.password = "$2b$12$j.hvS0zGfKRSvKPYdBSeruN5SWQVfTkMnpR.eRHRVLb.dxq2UmOOG"
        user.author_pseudonym = "rohit123"

        self._db.query(UsersModel).filter(
            UsersModel.username == user_schema.username).first.return_value = user

        response = self._users_usecase.sign_in(
            self._db, user_schema, UsersModel
        )
        self.assertFalse(response.status)
