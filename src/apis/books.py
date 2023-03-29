# Packages
from sqlalchemy.orm import Session
from typing import Union
from fastapi.routing import APIRouter
from fastapi import Request, Depends, Response, Header, UploadFile


# Modules
from utils.helper import Helper
from models.books import BooksModel
from models.users import UsersModel
from db.postgresql_db import get_db
from usecases.books import BooksUsecase
from usecases.users import UsersUsecase
from schemas.books import BooksAddSchema, BooksUpdateSchema


router = APIRouter(prefix="/books")


@router.get("/{book_id}")
def get_book_by_id(
    response: Response,
    book_id: int,
    db: Session = Depends(get_db),
    books_usecase: BooksUsecase = Depends(BooksUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    result = books_usecase.get_book_by_id(db, book_id, BooksModel)
    response.status_code = result.http_code
    if content_type == "application/xml":
        content = Helper.dict_to_xml(result.to_dict)
        return Response(content=content, media_type="application/xml")
    else:
        return result


@router.get("")
def list_books(
    response: Response,
    db: Session = Depends(get_db),
    books_usecase: BooksUsecase = Depends(BooksUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    result = books_usecase.list_books(db, BooksModel)
    response.status_code = result.http_code
    if content_type == "application/xml":
        content = Helper.dict_to_xml(result.to_dict)
        return Response(content=content, media_type="application/xml")
    else:
        return result


@router.post("")
def create_book(
    response: Response,
    book: BooksAddSchema,
    db: Session = Depends(get_db),
    books_usecase: BooksUsecase = Depends(BooksUsecase),
    content_type: Union[str, None] = Header(default=None),
    token_payload: UsersModel = Depends(Helper.get_token_payload),
):
    result = books_usecase.create_book(db, book, BooksModel)
    response.status_code = result.http_code
    if content_type == "application/xml":
        content = Helper.dict_to_xml(result.to_dict)
        return Response(content=content, media_type="application/xml")
    else:
        return result


@router.put("/{book_id}")
def update_book(
    response: Response,
    book_id: int,
    book: BooksUpdateSchema,
    token_payload: UsersModel = Depends(Helper.get_token_payload),
    db: Session = Depends(get_db),
    books_usecase: BooksUsecase = Depends(BooksUsecase),
    content_type: Union[str, None] = Header(default=None),

):
    result = books_usecase.update_book(db, book_id, book, BooksModel)
    response.status_code = result.http_code
    if content_type == "application/xml":
        content = Helper.dict_to_xml(result.to_dict)
        return Response(content=content, media_type="application/xml")
    else:
        return result


@router.delete("/{book_id}")
def delete_book(
    response: Response,
    book_id: int,
    token_payload: UsersModel = Depends(Helper.get_token_payload),
    db: Session = Depends(get_db),
    books_usecase: BooksUsecase = Depends(BooksUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    result = books_usecase.delete_book(db, book_id, BooksModel)
    response.status_code = result.http_code
    if content_type == "application/xml":
        content = Helper.dict_to_xml(result.to_dict)
        return Response(content=content, media_type="application/xml")
    else:
        return result


@router.post("/upload")
def upload_cover_image(
    response: Response,
    file: UploadFile,
    token_payload: UsersModel = Depends(Helper.get_token_payload),
    books_usecase: BooksUsecase = Depends(BooksUsecase),
    content_type: Union[str, None] = Header(default=None),
):
    result = books_usecase.upload_cover_image(file)
    response.status_code = result.http_code
    if content_type == "application/xml":
        content = Helper.dict_to_xml(result.to_dict)
        return Response(content=content, media_type="application/xml")
    else:
        return result
