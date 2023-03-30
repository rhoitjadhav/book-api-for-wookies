# Packages
from typing import Union
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from fastapi import Depends, Response, Header
from fastapi.security import OAuth2PasswordRequestForm


# Modules
from utils.helper import Helper
from models.users import UsersModel
from db.postgresql_db import get_db
from usecases.users import UsersUsecase
from schemas.users import UsersSignInSchema, UsersSignUpSchema


router = APIRouter(prefix="/users")


@router.post("/sign-in")
def sign_in(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    users_usecase: UsersUsecase = Depends(UsersUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    user = UsersSignInSchema(username=form_data.username,
                             password=form_data.password)
    result = users_usecase.sign_in(db, user, UsersModel)
    if not result.status:
        return result

    response.status_code = result.http_code
    if content_type == "application/xml":
        content = Helper.dict_to_xml(result.data)
        return Response(content=content, media_type="application/xml")
    else:
        return result.data


@router.post("/sign-up")
def sign_up(
    response: Response,
    user: UsersSignUpSchema,
    db: Session = Depends(get_db),
    users_usecase: UsersUsecase = Depends(UsersUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    result = users_usecase.sign_up(db, user, UsersModel)
    response.status_code = result.http_code
    if content_type == "application/xml":
        content = Helper.dict_to_xml(result.to_dict)
        return Response(content=content, media_type="application/xml")
    else:
        return result
