# Packages
from fastapi import status
from typing import Dict
from fastapi import HTTPException


class JWTTokenError(HTTPException):
    """This exception is used for all the jwt token related errors"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Dict = {"WWW-Authenticate": "Bearer"}
    ) -> None:

        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UserNotFound(HTTPException):
    """This exception is used when username is not found in the token payload"""

    def __init__(
        self,
        status_code: status,
        detail: str,
        headers: Dict = {"WWW-Authenticate": "Bearer"}
    ) -> None:

        super().__init__(status_code=status_code, detail=detail, headers=headers)
