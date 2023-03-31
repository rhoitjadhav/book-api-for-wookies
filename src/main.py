# Packages
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Modules
from config import STATIC_FILES_PATH
from apis.apis import router as api_router


app = FastAPI()
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
