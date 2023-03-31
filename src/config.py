import os

# Static Files
STATIC_FILES_PATH = "static"

# JWT
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "secret-key")
AUTH_ALGORITHM = os.getenv("AUTH_ALGORITHM", "HS256")
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", 14400))

# Postgresql
SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL", "sqlite:///./books.db")
    # "SQLALCHEMY_DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/books")

FORBIDDEN_USERS = {"Darth Vader"}
