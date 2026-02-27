# 🚨 Débitos Técnicos - FastAPI Car Shop ERP

## 📋 Resumo Executivo

Este documento identifica e prioriza os principais débitos técnicos encontrados no projeto FastAPI Car Shop ERP, classificados por criticidade e impacto no sistema.

---

## 🔴 CRÍTICOS (Segurança e Funcionalidade)

### 1. 🔐 Segurança de Senhas - VULNERABILIDADE CRÍTICA
**Descrição**: Senhas são "hasheadas" com concatenação simples (`password + "notreallyhashed"`)
- **Arquivo**: `app/src/domain/user/service.py:19`
- **Código**: `fake_hashed_password = user.password + "notreallyhashed"`
- **Risco**: Senhas armazenadas como texto plano
- **Impacto**: Acesso não autorizado completo ao sistema
- **Prioridade**: 🚨 IMEDIATA

**Solução**:
```python
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

### 2. 🔑 JWT Inseguro - VULNERABILIDADE CRÍTICA
**Descrição**: Secret key hardcoded e decode com "secret" genérico
- **Arquivos**: 
  - `app/src/dependencies.py:6,13,17`
  - `app/src/routers/auth.py:10`
- **Código**: `SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"`
- **Risco**: Tokens podem ser forjados facilmente
- **Impacto**: Acesso não autorizado completo
- **Prioridade**: 🚨 IMEDIATA

**Solução**:
```python
import secrets
from python-dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
```

### 3. 🔍 Lógica de Autenticação Quebrada - FUNCIONALIDADE CRÍTICA
**Descrição**: Login compara senha plano com hash falso
- **Arquivo**: `app/src/routers/auth.py:34`
- **Código**: `if db_user and user.password == db_user.hashed_password:`
- **Impacto**: Sistema de login não funciona
- **Prioridade**: 🚨 IMEDIATA

**Solução**:
```python
from .security import verify_password

if db_user and verify_password(user.password, db_user.hashed_password):
    # Login válido
```

---

## 🟠 ALTOS (Qualidade e Manutenibilidade)

### 4. 📦 Dependências Desatualizadas
**Descrição**: Versões antigas com vulnerabilidades conhecidas
- **Problemas**:
  - Python 3.6-3.8 (EOL)
  - FastAPI 0.66.0 (atual: 0.104+)
  - SQLAlchemy 1.4.21 (atual: 2.0+)
- **Risco**: Vulnerabilidades de segurança e perda de suporte
- **Prioridade**: 🔥 ALTA

**Solução**:
```txt
# requirements.txt atualizado
fastapi>=0.104.0
sqlalchemy>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
```

### 5. 🗄️ Configuração de Database Insegura
**Descrição**: Credenciais hardcoded no código fonte
- **Arquivo**: `app/src/database.py:11`
- **Código**: `SQLALCHEMY_DATABASE_URL = "postgresql://skatesham:skatesham-github@localhost/skatesham"`
- **Risco**: Exposição de credenciais em repositório
- **Prioridade**: 🔥 ALTA

**Solução**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
```

### 6. 🏗️ Import Faltando - ERRO DE COMPILAÇÃO
**Descrição**: Import JWT ausente em auth.py
- **Arquivo**: `app/src/routers/auth.py:24`
- **Erro**: `NameError: name 'jwt' is not defined`
- **Impacto**: Runtime error
- **Prioridade**: 🔥 ALTA

**Solução**:
```python
import jwt  # Adicionar no topo do arquivo
```

---

## 🟡 MÉDIOS (Performance e Boas Práticas)

### 7. 🔄 Middleware de Database Ineficiente
**Descrição**: Session criada para cada request sem pooling otimizado
- **Arquivo**: `app/main.py:56-69`
- **Problema**: Conexões não reutilizadas
- **Impacto**: Performance e resource leaks
- **Prioridade**: 📈 MÉDIA

**Solução**:
```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### 8. 📝 Validação de Dados Manual
**Descrição**: Validação repetitiva nos routers
- **Exemplo**: `app/src/routers/sales.py:28-40`
- **Problema**: Código duplicado e erros
- **Impacto**: Manutenibilidade e bugs
- **Prioridade**: 📈 MÉDIA

**Solução**:
```python
from pydantic import validator

class SaleCreate(BaseModel):
    car_id: int
    buyer_id: int
    seller_id: int
    
    @validator('car_id')
    def validate_car_exists(cls, v):
        # Validação automática
        return v
```

### 9. 🧪 Testes de Segurança Ausentes
**Descrição**: Coverage 93% mas sem testes de segurança
- **Problema**: Falha em detectar vulnerabilidades críticas
- **Impacto**: Falsa sensação de segurança
- **Prioridade**: 📈 MÉDIA

**Solução**:
```python
def test_password_hashing():
    """Testa se senhas estão sendo hasheadas corretamente"""
    pass

def test_jwt_validation():
    """Testa validação de tokens JWT"""
    pass
```

---

## 🟢 BAIXOS (Organização e Documentação)

### 10. 📁 Estrutura de Projeto Inconsistente
**Descrição**: Múltiplos padrões de organização
- **Problemas**:
  - Services misturados com repositories
  - Conversores separados desnecessariamente
- **Impacto**: Dificuldade de manutenção
- **Prioridade**: 📚 BAIXA

### 11. 📚 Documentação Desatualizada
**Descrição**: README refere-se a versões EOL
- **Problema**: Python 3.6-3.8 no setup
- **Impacto**: Setup problemático para novos devs
- **Prioridade**: 📚 BAIXA

### 12. 🔧 Configuração de Ambiente Incompleta
**Descrição**: `.env` referenciado mas não existe
- **Arquivo**: `.env.example` ausente
- **Impacto**: Setup quebrado
- **Prioridade**: 📚 BAIXA

---

## 🎯 Plano de Ação Sugerido

### 🚀 Fase 1: Segurança Imediata (1-2 dias)
1. ✅ Implementar hashing real de senhas
2. ✅ Mover secrets para environment variables
3. ✅ Corrigir lógica de autenticação
4. ✅ Adicionar import JWT faltante

### 🔥 Fase 2: Atualização (3-5 dias)
1. ✅ Atualizar dependências principais
2. ✅ Mover configurações para .env
3. ✅ Criar .env.example
4. ✅ Atualizar README

### 📈 Fase 3: Qualidade (1-2 semanas)
1. ✅ Implementar database pooling
2. ✅ Refatorar validações para Pydantic
3. ✅ Adicionar testes de segurança
4. ✅ Implementar logging

### 📚 Fase 4: Organização (2-3 semanas)
1. ✅ Reorganizar estrutura de pastas
2. ✅ Documentar arquitetura
3. ✅ Criar guias de desenvolvimento
4. ✅ Setup CI/CD

---

## 📊 Métricas de Sucesso

### Antes vs Depois
| Métrica | Antes | Depois (Meta) |
|---------|-------|---------------|
| Vulnerabilidades Críticas | 3 | 0 |
| Dependências Atualizadas | 20% | 95% |
| Coverage de Segurança | 0% | 80% |
| Tempo de Setup | 2h | 30min |

---

## 🔗 Recursos Úteis

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLAlchemy 2.0 Migration](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [Python Security Guidelines](https://python-security.readthedocs.io/)

---

**Última atualização**: 27/02/2026  
**Responsável**: Equipe de Desenvolvimento  
**Revisão**: Trimestral
