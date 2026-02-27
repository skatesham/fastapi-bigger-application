# FastAPI Car Shop ERP

[![codecov](https://codecov.io/gh/carshop/fastapi-erp/branch/main/graph/badge.svg)](https://codecov.io/gh/carshop/fastapi-erp)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.133.1-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.47-blue.svg)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.12.5-orange.svg)](https://docs.pydantic.dev/)

Professional REST API ERP system for car shop management built with FastAPI 0.133, SQLAlchemy 2.0, and modern Python patterns.

---

## ✨ Features

- 🚀 **FastAPI 0.133.1** - Latest stable version with modern patterns
- 🗄️ **SQLAlchemy 2.0.47** - Modern ORM with async support
- 🔐 **Professional Security** - JWT with core.security module
- 📊 **Pydantic V2.12.5** - Modern data validation and serialization
- 🏗️ **Clean Architecture** - Professional structure with core modules
- 🧪 **Comprehensive Testing** - Tests separated from application code
- 📝 **Auto Documentation** - Swagger/OpenAPI with `/docs`
- 🔧 **Professional Tooling** - Black, isort, mypy, pytest, coverage
- 🎯 **Dependency Injection** - FastAPI Annotated patterns
- 📦 **Modern Packaging** - pyproject.toml with professional setup
- 🔒 **Security Best Practices** - passlib, bcrypt, secure JWT handling

---

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.133.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.47
- **Configuration**: Pydantic Settings V2
- **Authentication**: JWT with python-jose[cryptography]
- **Validation**: Pydantic V2.12.5 + Pydantic Settings 2.13.1
- **Testing**: pytest 9.0.2 + pytest-asyncio 1.3.0 + pytest-cov 7.0.0
- **Code Quality**: Black 26.1.0, isort 8.0.0, flake8 7.3.0, mypy 1.19.1
- **Security**: passlib[bcrypt] 1.7.4, python-multipart 0.0.6
- **Database Tools**: psycopg2-binary 2.9.0, alembic 1.12.0
- **Documentation**: Auto-generated Swagger/OpenAPI
- **Architecture**: Clean API structure with v1 versioning

---

## 🏗️ Project Structure

```
fastapi-bigger-application/
├── app/                    # Application source code
│   ├── src/
│   │   ├── api/           # API layer (v1)
│   │   │   ├── deps.py    # Dependencies injection
│   │   │   ├── converters/ # Response converters
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/          # Core modules
│   │   │   ├── config.py  # Pydantic Settings
│   │   │   ├── database.py # Database setup
│   │   │   └── security.py # JWT & auth
│   │   ├── domain/        # Business logic
│   │   └── internal/      # Internal utilities
│   └── main.py           # Application entry point
├── tests/                # Test suite (external)
├── pyproject.toml       # Modern Python packaging
├── requirements.txt     # Dependencies
├── setup.cfg            # Flake8 configuration
├── .coveragerc          # Coverage configuration
└── .env.example        # Environment template
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/carshop/fastapi-erp.git
cd fastapi-erp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start the application
uvicorn app.main:app --reload
```

### Environment Configuration

Create `.env` file based on `.env.example`:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# CORS
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 📚 API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_jwt.py -v
```

---

## 🔧 Development

### Code Quality

```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint
flake8 app/ tests/

# Type checking
mypy app/

# Security check
bandit -r app/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Downgrade
alembic downgrade -1
```

---

## 📦 Deployment

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Production

```bash
# Install production dependencies
pip install -e .

# Run with Gunicorn (recommended for production)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login

### Resources
- `GET /api/v1/buyers/` - List buyers
- `POST /api/v1/buyers/` - Create buyer
- `GET /api/v1/cars/` - List cars
- `POST /api/v1/cars/` - Create car
- `GET /api/v1/sales/` - List sales
- `POST /api/v1/sales/` - Create sale

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

---

## Source Documentation

- [FastAPI](https://fastapi.tiangolo.com/)
- [Bigger Application](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Testing](https://fastapi.tiangolo.com/tutorial/testing/)  
- [Pydantic](https://pydantic-docs.helpmanual.io/)  
- [SQL Relational Database SQLAlchemy by FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=databa#sql-relational-databases)
- [SQLAlchemy 1.4](https://docs.sqlalchemy.org/en/14/tutorial/engine.html)  
- [FastAPI "Real world example app"](https://github.com/nsidnev/fastapi-realworld-example-app)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Created by
> Sham Vinicius Fiorin

**Built with ❤️ using FastAPI and modern Python patterns**

---