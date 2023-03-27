# Packages
from fastapi import APIRouter

# Modules
from .users import router as users

router = APIRouter()

router.include_router(users)
