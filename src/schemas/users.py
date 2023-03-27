# Packages
from typing import Optional
from pydantic import BaseModel


class UsersSignInSchema(BaseModel):
    username: str
    password: str


class UsersSignUpSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    author_pseudonym: Optional[str]
