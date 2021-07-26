# Fast API

## Requirements
You'll must have installed:
- Python 3.6+
- Virtualenv for Python3.6+
- Docker
- Docker-compose

## Setup Project

__Create Virtual Environment__
```bash
sudo apt-get install python-virtualenv
virtualenv -p python3.6 env
# Or 
sudo apt-get install python3.6-venv python3.6-dev
python3.6 -m venv env
```

__Activating virtual environment__
```bash
source env/bin/activate 
```
__Install depedencies__
```bash
pip install -r requirements.txt 
```

## Running Application

For start application, run command below:
```bash
uvicorn app.main:app --reload
```

## Using application local
The application will get started in http://127.0.0.1:8000.  

Acessing documentation on http://127.0.0.1:8000/docs.

Another documentation option could be
http://127.0.0.1:8000/redoc

__App Authentication__
- token = jessica
- x_token = fake-super-secret-token

__Accessing Database with Adminer__  
The database can be accessed by adminer on http://127.0.0.1:9000 using postgres and credentials tinnova/tinnova123(user/password).

## Testing

__For test run__  
```bash
pytest
```

### Source Documentation
- [FastAPI](https://fastapi.tiangolo.com/)

- [Bigger Application](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

- [SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/)
