# Book API for wookies

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

<http://localhost:8000/docs>

## Running Unit & API Tests

```commandline
cd src
python test.py
python test_apis.py
```

## Deployment

### 1. Docker Compose

Docker compose will first build the api image using Dockerfile and then run the postgres and api containers

```commandline
docker compose up
```

### 2. Kubernetes

For deployment in Kubernetes cluster you can refer the `k8s` folder for `.yaml` based configuration files.
Assuming you have minikube cluster setup and a kubectl, then you can simply run the following commands to
deploy the application and postgresql.

```commandline
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/postgres-deployment.yaml
```
