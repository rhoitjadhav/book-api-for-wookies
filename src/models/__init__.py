# Modules
from .users import UsersModel
from .books import BooksModel
from db.postgresql_db import Base, engine

Base.metadata.create_all(engine)
