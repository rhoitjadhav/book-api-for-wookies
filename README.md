# WorkGenius-Challenge

## Requirements

- Python (3.8+)
- FastAPI
- Postgresql/Sqlite

## Running Application

First, we need to create virtual environment and install dependencies.
After successful installation, we will run the backend application.
Following are the commands which does the same.

```commandline
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

Output:

```commandline
INFO:     Started server process [16967]
INFO:     Waiting for application startup.
Database created
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Test whether the application is started properly or not, just hit the docs API link from below and 
you should see the swagger api response on browser.

http://localhost:8000/docs

## Running Unit & API Tests

```commandline
cd src
python test.py
python test_apis.py
```

## Deployment

For deployment, we first need to build docker image. After successfully building image,
we can now simply run the docker image in a container.

Docker build and run commands:

```commandline
docker build -t test/test:latest -f Dockerfile .
docker run -d --name backend-app -p 8000:8000 test/test:latest
```

In k8s folder, there are .yaml files for deploying the application on kubernetes cluster.
