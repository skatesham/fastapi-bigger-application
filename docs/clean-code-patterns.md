# 🧹 Clean Code & FastAPI Patterns - Débitos Técnicos

## 📋 Resumo
Foco exclusivo em clean code, padrões FastAPI e boas práticas de arquitetura.

---

## 🔴 CRÍTICOS (Violations of Clean Code & Patterns)

### 1. 🏗️ **Arquitetura Inconsistente** - VIOLAÇÃO CRÍTICA
**Problema**: Mistura de responsabilidades e padrões inconsistentes
- **Arquivos**: `app/src/domain/*/service.py`, `app/src/routers/converter/`
- **Issues**:
  - Services com lógica de repository
  - Conversores separados desnecessariamente
  - Routers com validação manual
- **Violations**: SRP, DRY, Clean Architecture

**Solução Padrão FastAPI**:
```python
# ✅ Padrão correto
app/
├── api/
│   ├── endpoints/          # Routers puros
│   └── dependencies.py     # Dependencies injetáveis
├── core/
│   ├── config.py          # Configurações
│   └── security.py        # Lógica de segurança
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic models
├── crud/                  # Database operations
└── services/              # Business logic
```

### 2. 📝 **Validação Manual em Routers** - VIOLAÇÃO CRÍTICA
**Problema**: Lógica de validação espalhada nos routers
- **Arquivo**: `app/src/routers/sales.py:28-40`
- **Código**: Validações manuais com múltiplos if's
- **Violation**: Single Responsibility, DRY

**Solução Padrão FastAPI**:
```python
# ✅ Usar Pydantic para validação
class SaleCreate(BaseModel):
    car_id: int
    buyer_id: int
    seller_id: int
    
    @validator('car_id')
    def car_must_exist(cls, v, values, **kwargs):
        # Validação automática
        return v

@router.post("/", response_model=Sale)
async def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Router limpo, só orquestração
    return crud.create_sale(db=db, sale=sale)
```

### 3. 🔧 **Dependencies Injetadas Manualmente** - VIOLAÇÃO CRÍTICA
**Problema**: Middleware para database session
- **Arquivo**: `app/main.py:56-69`
- **Issue**: Session manual em middleware
- **Violation**: Dependency Injection Pattern

**Solução Padrão FastAPI**:
```python
# ✅ Dependency Injection nativo
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Uso nos routers
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)
```

---

## 🟠 ALTOS (Code Quality & Maintainability)

### 4. 📦 **Imports e Estrutura Desorganizados** - ALTO
**Problema**: Imports inconsistentes e estrutura confusa
- **Arquivos**: Múltiplos arquivos com imports desorganizados
- **Issues**:
  - Imports relativos e absolutos misturados
  - Imports não agrupados por tipo
- **Violation**: PEP 8, Readability

**Solução Padrão**:
```python
# ✅ Imports organizados (PEP 8)
# Standard library
from typing import List, Optional
from datetime import datetime

# Third party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Local imports
from app.core.config import settings
from app.crud import user as user_crud
from app.schemas import user as user_schema
from app.api.deps import get_current_user, get_db
```

### 5. 🔄 **Lógica de Negócio em Routers** - ALTO
**Problema**: Business logic misturada com presentation
- **Arquivo**: `app/src/routers/sales.py:42`
- **Código**: `stock_service.buy_car_from_stock()` no router
- **Violation**: Clean Architecture, Separation of Concerns

**Solução Padrão FastAPI**:
```python
# ✅ Service Layer
class SaleService:
    def create_sale(self, db: Session, sale_data: SaleCreate) -> Sale:
        # Business logic aqui
        self.validate_entities(db, sale_data)
        self.update_stock(db, sale_data.car_id)
        return self.create_sale_record(db, sale_data)

# ✅ Router limpo
@router.post("/", response_model=Sale)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    service: SaleService = Depends(get_sale_service)
):
    return service.create_sale(db=db, sale_data=sale)
```

### 6. 🏷️ **Naming Inconsistente** - ALTO
**Problema**: Nomes que não seguem convenções
- **Issues**:
  - `db_sale` vs `sale`
  - `get_user` vs `read_user`
  - Funções com nomes genéricos
- **Violation**: Clean Code - Meaningful Names

**Solução Padrão**:
```python
# ✅ Nomes consistentes e descritivos
def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by primary key"""
    return db.query(User).filter(User.id == user_id).first()

def create_user_with_profile(db: Session, user_data: UserCreate) -> User:
    """Create user with associated profile"""
    pass
```

---

## 🟡 MÉDIOS (Modern FastAPI Patterns)

### 7. 🚀 **Falta de Pydantic V2 Features** - MÉDIO
**Problema**: Não usando features modernas do Pydantic
- **Issues**:
  - Validação com decorator @validator (legado)
  - Sem uso de Field validators
  - Config deprecated

**Solução Moderna**:
```python
# ✅ Pydantic V2
from pydantic import BaseModel, Field, field_validator

class UserCreate(BaseModel):
    email: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)
    
    @field_validator('email')
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
    
    model_config = ConfigDict(str_strip_whitespace=True)
```

### 8. 🔄 **Falta de Async/Await** - MÉDIO
**Problema**: Código síncrono em FastAPI assíncrono
- **Impacto**: Performance subótima
- **Violation**: FastAPI Best Practices

**Solução Padrão**:
```python
# ✅ Async patterns
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### 9. 📝 **Falta de Type Hints Completos** - MÉDIO
**Problema**: Type hints incompletos ou ausentes
- **Impacto**: Perda de benefícios do TypeScript-like Python
- **Violation**: Modern Python Standards

**Solução Padrão**:
```python
# ✅ Type hints completos
from typing import List, Optional, Generator
from sqlalchemy.orm import Session

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[User]:
    """Get users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()
```

---

## 🟢 BAIXOS (Code Organization)

### 10. 📁 **Estrutura de Pastas Subótima** - BAIXO
**Problema**: Estrutura não segue padrões FastAPI
- **Issue**: `app/src/domain/` vs `app/models/`
- **Violation**: FastAPI Project Structure

**Solução Padrão**:
```
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py      # APIRouter
│   │       └── endpoints/
│   │           ├── users.py
│   │           └── items.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── base.py
│   │   ├── user.py
│   │   └── item.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   └── services/
│       ├── user.py
│       └── item.py
```

### 11. 🧪 **Testes sem Padrões Modernos** - BAIXO
**Problema**: Testes sem seguir padrões FastAPI
- **Issues**:
  - Sem uso de TestClient
  - Testes síncronos para app assíncrono
  - Fixtures não reutilizáveis

**Solução Padrão**:
```python
# ✅ Testes modernos
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
```

### 12. 📚 **Falta de Documentação de Código** - BAIXO
**Problema**: Docstrings ausentes ou inconsistentes
- **Impacto**: Dificuldade de manutenção
- **Violation**: Python Documentation Standards

**Solução Padrão**:
```python
# ✅ Docstrings Google Style
def create_user(
    db: Session,
    user_data: UserCreate
) -> User:
    """Create a new user in the database.
    
    Args:
        db: Database session
        user_data: User creation data with email and password
        
    Returns:
        Created user instance
        
    Raises:
        IntegrityError: If email already exists
    """
    pass
```

---

## 🎯 Plano de Refatoração (Clean Code Focus)

### 🚀 Fase 1: Padrões FastAPI Essenciais
1. ✅ Implementar Dependency Injection correta
2. ✅ Mover validações para Pydantic
3. ✅ Separar routers de business logic
4. ✅ Criar estrutura de pastas padrão

### 🔥 Fase 2: Clean Code
1. ✅ Refatorar naming conventions
2. ✅ Adicionar type hints completos
3. ✅ Organizar imports (PEP 8)
4. ✅ Adicionar docstrings consistentes

### 📈 Fase 3: Modernização
1. ✅ Migrar para Pydantic V2
2. ✅ Implementar async/await
3. ✅ Usar Field validators
4. ✅ Config com Pydantic Settings

### 📚 Fase 4: Qualidade
1. ✅ Testes com padrões modernos
2. ✅ Linting e formatting
3. ✅ Pre-commit hooks
4. ✅ CI/CD com quality gates

---

## 📊 Métricas de Clean Code

| Métrica | Antes | Depois (Meta) |
|---------|-------|---------------|
| Complexidade Ciclomática | 15 | <5 |
| Coverage | 93% | 95% |
| Type Coverage | 60% | 95% |
| Linting Issues | 50+ | 0 |
| Code Smells | 20+ | 0 |

---

## 🔗 Recursos FastAPI Clean Code

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Clean Code Python](https://github.com/zedr/clean-code-python)
- [Pydantic V2 Migration](https://docs.pydantic.dev/latest/migration/)
- [FastAPI Project Structure](https://github.com/zhanymkanov/fastapi-best-practices)

---

**Foco**: Clean Code, FastAPI Patterns, Modern Python  
**Excluídos**: Versões, segurança, infraestrutura
