# Fast API

![coverage](https://img.shields.io/badge/coverage-95%25-darkgreen)

## Requirements
You'll must have installed:
- [Python 3.6+](https://www.python.org/downloads/)
- [Virtual Environments with Python3.6+](https://docs.python.org/3/tutorial/venv.html)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)

## Setup Project

Create virtual environment
```bash
python3 -m venv env
```

Activating created virtual environment
```bash
source env/bin/activate 
```
Install app depedencies
```bash
pip install -r requirements.txt 
```

## Running Application

Starting database (postgres:alpine3.14)
```bash
docker-compose up
```

Starting application, run:
```bash
uvicorn app.main:app --reload
```

##### Obs: It's possible to configure the database by environment variable as:
##### `export URI_DB="postgresql://user-name:password@host-name/database-name"`  


## Acessing on local
The application will get started in http://127.0.0.1:8000  

Swagger Documentation: http://127.0.0.1:8000/docs

Redoc Documentation: http://127.0.0.1:8000/redoc

Database Adminer: http://127.0.0.1:9000
- credentials tinnova/tinnova123(user/password).

If required authentication on routes add headers:
- token = jessica
- x_token = fake-super-secret-token

## Testing

__For run tests__  
```bash
pytest
```

__For run tests with coverage report__  
```bash
pytest --cov=app app/test/
```

## Development

For update dependencies on `requirements.txt`, run:  

```bash
pip freeze > requirements.txt
```


### Source Documentation
- [FastAPI](https://fastapi.tiangolo.com/)

- [Bigger Application](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

- [SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/)

- [Testing](https://fastapi.tiangolo.com/tutorial/testing/)
