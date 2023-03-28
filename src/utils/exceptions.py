# Packages
from fastapi import status
from typing import Dict
from fastapi import HTTPException


class JWTTokenError(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Dict = {"WWW-Authenticate": "Bearer"}
    ) -> None:

        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UserNotFound(HTTPException):
    def __init__(
        self,
        status_code: status,
        detail: str,
        headers: Dict = {"WWW-Authenticate": "Bearer"}
    ) -> None:

        super().__init__(status_code=status_code, detail=detail, headers=headers)
