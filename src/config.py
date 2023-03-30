import os

# Static Files 
STATIC_FILES_PATH = "static"

# JWT
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "secret-key")
AUTH_ALGORITHM = os.getenv("AUTH_ALGORITHM", "HS256")
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", 14400))

# Postgresql
POSTGRESQL_HOST
POSTGRESQL_PORT
POSTGRESQL_USER
POSTGRESQL_PASSWORD
POSTGRESQL_DB
