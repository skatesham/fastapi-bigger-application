# FastAPI for Car Shop ERP

![coverage](https://img.shields.io/badge/coverage-93%25-darkgreen)  

This rest api is a kind of ERP of car shop.  
App is available on cloud by https://car-shop-fastapi.herokuapp.com/docs.

## Requirements
You'll must have installed:
- [Python 3.6+](https://www.python.org/downloads/)
- [Virtual Environments with Python3.6+](https://docs.python.org/3/tutorial/venv.html)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)
___
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
pip install -r requirements-local.txt 
```
___
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
##### `export DB_URL="postgresql://user-name:password@host-name/database-name"`  


## Acessing on local
The application will get started in http://127.0.0.1:8000  

Swagger Documentation: http://127.0.0.1:8000/docs

Redoc Documentation: http://127.0.0.1:8000/redoc

Database Adminer: http://127.0.0.1:9000
- credentials tinnova/tinnova123(user/password).

If required authentication on routes add headers:
- token = jessica
- x_token = fake-super-secret-token
___
## Testing

__For run tests__  
```bash
pytest
```

__For run tests with coverage report__  
```bash
pytest --cov=app app/test/
```
___
## Development

For update dependencies on `requirements.txt`, run:  

```bash
pip freeze > requirements.txt (requires extra changes)
```
___
## Deploy On Heroku

__Requirements__  

- [Heroku Cli](https://devcenter.heroku.com/articles/heroku-cli)

__Install Heroku Cli__  
```
sudo snap install --classic heroku
```

__Deploy__

**Case is activated automatic deploy for `master` branch, just commit on `master` branch,  
instead make manual deploy from Heroku Cli, like below**  
```
heroku login
heroku git:remote -a car-shop-fastapi
git add .
git commit -m "Deploy on heroku"
git push origin master
git push heroku master
```
 ___

### Source Documentation
- [FastAPI](https://fastapi.tiangolo.com/)

- [Bigger Application](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

- [SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/)

- [Testing](https://fastapi.tiangolo.com/tutorial/testing/)  

- [Pydantic](https://pydantic-docs.helpmanual.io/)  

- [SQL Relational Database SQLAlchemy by FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=databa#sql-relational-databases)

- [SQLAlchemy 1.4](https://docs.sqlalchemy.org/en/14/tutorial/engine.html)  

- [FastAPI "Real world example app"](https://github.com/nsidnev/fastapi-realworld-example-app)  

