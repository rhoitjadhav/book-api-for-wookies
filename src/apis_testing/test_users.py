# Packages
import requests
import unittest
from fastapi import status

# Modules
from utils.helper import Helper


class TestUsersAPI(unittest.TestCase):
    # Note: There will lot of other test cases, however for the simplicity
    # there few of them that will be helpful to test the code.
    _host = "http://localhost:8000"

    @classmethod
    def setUpClass(cls):
        url = f"{cls._host}/api/users/sign-up"
        payload = {
            "first_name": "rohit",
            "last_name": "jadhav",
            "email": "rohit@gmail.com",
            "username": "rohit",
            "password": "1234",
            "author_pseudonym": "rohit123"
        }
        headers = {
            'Content-Type': 'application/json'
        }

        requests.post(url, headers=headers, json=payload)

    def test_sign_up_status_code(self):
        url = f"{self._host}/api/users/sign-up"
        payload = {
            "first_name": "rohit",
            "last_name": "jadhav",
            "email": Helper.generate_random_text(),
            "username": Helper.generate_random_text(),
            "password": "1234",
            "author_pseudonym": Helper.generate_random_text()
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_sign_in_and_match_access_token_payload_username(self):
        url = f"{self._host}/api/users/sign-in"
        payload = {"username": "rohit", "password": "1234"}

        response = requests.post(url, data=payload).json()
        token_payload = Helper.get_token_payload(response["access_token"])
        self.assertEqual(payload["username"], token_payload["username"])

    def test_user_sign_in_with_incorrect_password(self):
        url = f"{self._host}/api/users/sign-in"
        payload = {"username": "rohit", "password": "wrong-password"}

        response = requests.post(url, data=payload)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
