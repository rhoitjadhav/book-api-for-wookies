# Packages
import json
import requests
import unittest
from fastapi import status


class TestBooksAPI(unittest.TestCase):
    _host = "http://localhost:8000"

    # Access token expire on 9 Apr 2023
    _access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb2hpdCIsImVtYWlsIjoicm9oaXRAZ21haWwuY29tIiwidXNlcm5hbWUiOiJyb2hpdCIsImF1dGhvcl9wc2V1ZG9ueW0iOiJyb2hpdDEyMyIsImV4cCI6MTY4MTAxMzYxMX0.py7aIPrCxXgoaq9cXJ7eV4fpq6k89zW3N8R6xHosXJE"

    def test_get_book_by_id(self):
        url = f"{self._host}/api/books/1"
        response = requests.get(url).json()
        self.assertTrue(response["status"])

    def test_create_book(self):
        url = f"{self._host}/api/books"
        payload = {
            "title": "Bhagvadgit",
            "description": "Bhagvadgit As it is",
            "cover_image": "M5VRR1_requirements.txt",
            "price": 180,
            "author": "A.C. Bhaktivedant Sri Prabhupada"
        }
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=payload).json()
        self.assertTrue(response["status"])

    def test_upload_cover_image_with_empty_image(self):
        url = f"{self._host}/api/books/upload"
        headers = {
            'Authorization': f'Bearer {self._access_token}',
        }

        response = requests.post(url, headers=headers)
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY,
                         response.status_code)

    def test_create_book_with_missing_author_in_payload(self):
        url = f"{self._host}/api/books"
        payload = {
            "title": "Bhagvadgit",
            "description": "Bhagvadgit: As it is",
            "cover_image": "M5VRR1_requirements.txt",
            "price": 180,
        }
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=payload)
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY,
                         response.status_code)

    def test_update_book_without_token(self):
        url = f"{self._host}/api/books/1"
        payload = {
            "title": "Bhagvadgit",
            "description": "Bhagvadgit: As it is",
            "cover_image": "M5VRR1_requirements.txt",
            "price": 180,
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.put(url, headers=headers, json=payload)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         response.status_code)
