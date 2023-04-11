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
            headers=None
    ) -> None:
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}

        super().__init__(status_code=status_code, detail=detail, headers=headers)
