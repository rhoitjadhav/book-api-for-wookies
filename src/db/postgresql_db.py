# Packages
import os
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
