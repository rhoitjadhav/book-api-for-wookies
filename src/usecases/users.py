# Packages
from typing import Type
from fastapi import status
from sqlalchemy.orm import Session

# Modules
from models.users import UsersModel
from utils.helper import ReturnValue, Helper
from schemas.users import UsersSignInSchema, UsersSignUpSchema
from config import (
    AUTH_SECRET_KEY,
    AUTH_ALGORITHM,
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
)


class UsersUsecase:
    @staticmethod
    def _is_username_exists(db: Session, user_model: Type[UsersModel], username: str):
        user = db.query(user_model).filter(
            user_model.username == username).first()
        if user:
            return True

        return False

    @staticmethod
    def _is_email_exists(db: Session, user_model: Type[UsersModel], email: str):
        user = db.query(user_model).filter(user_model.email == email).first()
        if user:
            return True

        return False

    @staticmethod
    def sign_in(db: Session, user_schema: UsersSignInSchema, user_model: Type[UsersModel]) -> ReturnValue:
        user = db.query(user_model).filter(
            user_model.username == user_schema.username).first()

        if not user or not Helper.verify_password(user_schema.password, user.password):
            return ReturnValue(False, status.HTTP_401_UNAUTHORIZED, "Username or password is wrong")

        payload = {
            "email": user.email,
            "username": user.username,
            "author_pseudonym": user.author_pseudonym
        }
        token = Helper.create_access_token(
            payload, AUTH_SECRET_KEY, AUTH_ALGORITHM, AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
        return ReturnValue(True, status.HTTP_200_OK, "User signed in", data={"access_token": token})

    @staticmethod
    def sign_up(db: Session, user_schema: UsersSignUpSchema, user_model: Type[UsersModel]) -> ReturnValue:
        if UsersUsecase._is_username_exists(db, user_model, user_schema.username):
            return ReturnValue(False, status.HTTP_409_CONFLICT, "Username already exists")

        if UsersUsecase._is_email_exists(db, user_model, user_schema.email):
            return ReturnValue(False, status.HTTP_409_CONFLICT, "Email already exists")

        user_schema.password = Helper.generate_hased_password(
            user_schema.password)
        user = user_model(**user_schema.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return ReturnValue(True, status.HTTP_200_OK, "User Signed up", data=user)
