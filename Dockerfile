FROM python:3.8.10

# Exposing port
EXPOSE 8000

# Environment Variables
ENV SQLALCHEMY_DATABASE_URL "sqlite:///./books.db"

# Copying source code
COPY ./requirements.txt /book-api-for-wookies-txzflq/
COPY ./src/ /book-api-for-wookies-txzflq/src

# Installing dependencies
RUN pip install -r /book-api-for-wookies-txzflq/requirements.txt

# Setting working directory
WORKDIR /book-api-for-wookies-txzflq/src

# Running application
CMD ["python", "main.py"]