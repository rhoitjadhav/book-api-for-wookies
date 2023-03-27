# Packages
from sqlalchemy.orm import Session
from typing import Union
from fastapi.routing import APIRouter
from fastapi import Request, Depends, Response, Header


# Modules
from utils.helper import Helper
from models.users import UsersModel
from db.postgresql_db import get_db
from usecases.users import UsersUsecase
from schemas.users import UsersSignInSchema, UsersSignUpSchema


router = APIRouter(prefix="/users")


@router.post("/sign-in")
def sign_in(
    user: UsersSignInSchema,
    db: Session = Depends(get_db),
    users_usecase: UsersUsecase = Depends(UsersUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    result = users_usecase.sign_in(db, user, UsersModel)
    if content_type == "application/xml":
        response = Helper.dict_to_xml(result.to_dict)
        return Response(content=response, media_type="application/xml")
    else:
        return result


@router.post("/sign-up")
def sign_up(
    user: UsersSignUpSchema,
    db: Session = Depends(get_db),
    users_usecase: UsersUsecase = Depends(UsersUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    result = users_usecase.sign_up(db, user, UsersModel)
    if content_type == "application/xml":
        response = Helper.dict_to_xml(result.to_dict)
        return Response(content=response, media_type="application/xml")
    else:
        return result
