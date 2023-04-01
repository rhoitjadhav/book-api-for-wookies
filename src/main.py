# Packages
import os
import json
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas.books import BooksAddSchema
from pydantic.error_wrappers import ValidationError

# Modules
from utils.helper import Helper
from config import STATIC_FILES_PATH
from apis.apis import router as api_router


app = FastAPI()


# Validation Error Handler
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/xml":
        json_response = jsonable_encoder(
            {"detail": exc.errors()})
        return Response(content=Helper.dict_to_xml(json_response, False),
                        media_type="application/xml",
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": exc.errors()}),
    )

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    # Database
    import models  # noqa: F401
    print("Database created")

    # Create static folder
    if not os.path.exists(STATIC_FILES_PATH):
        os.makedirs(STATIC_FILES_PATH)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
