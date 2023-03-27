# Packages
import unittest
from unittest.mock import MagicMock, patch


# Modules
from usecases.users import UsersUsecase


class TestUsers(unittest.TestCase):
    _users_usecase = UsersUsecase()

    def test_user_sign_up(self):
        pass

    def test_user_sign_in_with_correct_username_password():
        pass

    def test_user_sign_in_with_incorrect_username():
        pass

    def test_user_sign_in_with_incorrect_password():
        pass
