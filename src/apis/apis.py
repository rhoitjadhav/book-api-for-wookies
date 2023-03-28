# Packages
from fastapi import APIRouter

# Modules
from .users import router as users
from .books import router as books

router = APIRouter(prefix="/api")

router.include_router(users)
router.include_router(books)
