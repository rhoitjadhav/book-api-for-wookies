# Packages
from typing import Union
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from fastapi import Depends, Response, Header, Request


# Modules
from utils.helper import Helper
from models.users import UsersModel
from db.postgresql_db import get_db
from usecases.users import UsersUsecase
from schemas.users import UsersSignInSchema, UsersSignUpSchema


router = APIRouter(prefix="/users")


@router.post("/sign-in")
async def sign_in(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    users_usecase: UsersUsecase = Depends(UsersUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    if "form" in content_type:
        payload = dict(await request.form())

    else:
        payload = await Helper.convert_request_body_to_dict(
            request, content_type, "user"
        )

    user = UsersSignInSchema(**payload)
    result = users_usecase.sign_in(db, user, UsersModel)
    response.status_code = result.http_code

    result_dict = result.to_dict()
    result_dict.update(result_dict["data"])
    result_dict["data"] = []

    if content_type == "application/xml":
        content = Helper.dict_to_xml(result_dict)
        return Response(content=content, media_type="application/xml", status_code=result.http_code)

    return result_dict


@router.post("/sign-up")
async def sign_up(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    users_usecase: UsersUsecase = Depends(UsersUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    body_dict = await Helper.convert_request_body_to_dict(
        request, content_type, "user"
    )
    user = UsersSignUpSchema(**body_dict)
    result = users_usecase.sign_up(db, user, UsersModel)
    response.status_code = result.http_code
    if content_type == "application/xml":
        result.data = Helper.model_to_dict(result.data)
        content = Helper.dict_to_xml(result.to_dict())
        return Response(content=content, media_type="application/xml", status_code=result.http_code)

    return result
