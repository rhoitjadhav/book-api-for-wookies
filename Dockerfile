FROM python:3.8.10

# Exposing port
EXPOSE 8000

# Environment Variables
ENV POSTGRESQL_HOST "localhost"
ENV POSTGRESQL_PORT 5432
ENV POSTGRESQL_USER "user"
ENV POSTGRESQL_PASSWORD "password"
ENV POSTGRESQL_DB "books"

# Copying source code
COPY ./requirements.txt /book-api-for-wookies-txzflq/
COPY ./src/ /book-api-for-wookies-txzflq/src

# Installing dependencies
RUN pip install -r /book-api-for-wookies-txzflq/requirements.txt

# Setting working directory
WORKDIR /book-api-for-wookies-txzflq/src

# Running application
CMD ["python", "main.py"]