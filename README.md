# 🚗 FastAPI Bigger Application — Car Shop Demo

<p align="center">
  <img src="assets/readme-header.svg" alt="FastAPI Bigger Application — Car Shop Demo" width="960" />
</p>

Uma demonstração da arquitetura **Bigger Applications** do FastAPI, usando o cenário de uma loja de carros. O foco é mostrar uma base organizada para APIs, e não entregar um ERP de produção completo.

## ✨ O que este projeto demonstra

Uma base prática para desenvolver uma API de gestão de loja de carros com execução local reproduzível. Ela já inclui cadastro e consulta de usuários, compradores, vendedores, carros, estoque e vendas, documentação interativa e um banco que pode ser criado do zero com migrations e dados de exemplo.

O valor do projeto é permitir que uma pessoa nova no time execute a aplicação com poucos comandos, encontre as rotas em `/docs` e tenha a mesma estrutura de banco nos ambientes de desenvolvimento.

### 🧰 Ferramentas utilizadas

- **FastAPI** para rotas HTTP e documentação OpenAPI automática.
- **SQLAlchemy** para mapear os modelos Python para PostgreSQL.
- **Alembic** para versionar mudanças no schema do banco.
- **Pydantic** para validar dados de entrada e saída.
- **PostgreSQL** como banco relacional.
- **Docker Compose** para executar API, banco e Adminer juntos.
- **Make** para concentrar os comandos do dia a dia.
- **Pytest** para testes automatizados.

### 🧩 Padrões aplicados

- **Separação por domínio**: cada recurso possui modelos, schemas, repositório, serviço e endpoints.
- **Repository e service layers**: acesso ao banco e regras de negócio ficam separados das rotas HTTP.
- **Injeção de dependências**: sessões de banco e serviços são fornecidos às rotas de forma controlada.
- **Configuração por ambiente**: segredos e URLs ficam no `.env`, fora do código.
- **Migrations e seeds versionados**: schema e dados iniciais têm histórico, ordem e execução repetível.

## 🚀 Como usar

### 1️⃣ Instale os pré-requisitos

Para o caminho Docker, você precisa de Docker com Docker Compose e GNU Make. Python 3.11+ só é necessário para o desenvolvimento local. O Docker é o caminho recomendado porque já fornece o PostgreSQL.

Instale o Make no Linux caso ele não esteja disponível:

```bash
# Ubuntu, Debian e derivados
sudo apt update && sudo apt install -y make

# Windows (PowerShell, com Chocolatey)
choco install make
```

### 2️⃣ Crie o arquivo de ambiente

O Compose carrega o `.env` no container da API. Crie-o antes de executar comandos que iniciam a aplicação:

```bash
cp .env.example .env
```

Para desenvolvimento local, mantenha o `DATABASE_URL` com `localhost`. No Docker, o Compose substitui somente essa variável pela URL interna do serviço `db`; os demais valores, como `SECRET_KEY`, são lidos do `.env`.

### 3️⃣ Inicie com Docker

```bash
make docker-up
```

O comando cria os containers. Antes de iniciar a API, o container executa automaticamente as migrations do Alembic e os seeds pendentes.

### 🔗 Rotas e acessos de demonstração

| Serviço | Endereço | Acesso |
| --- | --- | --- |
| API | http://localhost:8000 | Health check: http://localhost:8000/health |
| Swagger UI | http://localhost:8000/docs | Execute e teste as rotas da API. |
| ReDoc | http://localhost:8000/redoc | Consulte a documentação em modo leitura. |
| Adminer | http://localhost:9000 | Sistema: `PostgreSQL`; servidor: `db`; usuário: `skatesham`; senha: `skatesham-github`; banco: `skatesham`. |

Depois de executar os seeds, use estas credenciais na rota `POST /api/v1/auth/login/` pelo Swagger:

```text
Usuário: admin@example.com
Senha: change-me
```

```bash
make docker-logs   # acompanhar logs da API
make docker-down   # parar os containers
make docker-reset  # parar e apagar o volume do banco
```

### 4️⃣ Desenvolvimento local opcional

Após concluir as etapas anteriores, instale as dependências Python. Para usar o banco no Docker e a API na sua máquina, deixe `make db-up` rodando em outro terminal.

```bash
python3 -m venv .venv
source .venv/bin/activate
make install

# Em outro terminal, inicie o banco via Docker
make db-up

# Aplica migrations, seeds e sobe a API localmente
make run
```

## 🛠️ Comandos Make

Execute `make help` para listar todos os comandos. Os principais são:

```bash
make install                         # instala dependências
make run                             # migration + seed + API local
make test                            # executa testes
make format                          # formata o código
make check                           # linter, tipos e testes

make db-up                           # inicia apenas PostgreSQL
make db-shell                        # abre psql no PostgreSQL

make migration-up                    # aplica migrations
make migration-down                  # reverte uma migration
make migration-new MESSAGE="add foo" # cria migration por autogenerate
make migration-current               # mostra a versão atual

make seed                            # aplica seeds pendentes

make docker-up                       # constrói e inicia tudo
make docker-down                     # para containers
make docker-logs                     # logs da API
make docker-shell                    # shell da API
```

## 🗄️ Banco de dados

As migrations ficam em [`db/migration/versions`](db/migration/versions), uma por tabela. O schema não é criado pela aplicação no startup: use sempre o Alembic.

Os seeds ficam em [`db/seed/versions`](db/seed/versions), pareados às revisões das tabelas. Cada seed é registrado na tabela `seed_history`, portanto `make seed` pode ser executado repetidamente sem duplicar dados.

O conjunto inicial cria um usuário, uma compradora, uma vendedora, três carros, seus registros de estoque e uma venda de demonstração. As credenciais de acesso estão na seção **Rotas e acessos de demonstração**.

Essas credenciais e dados são exclusivamente para desenvolvimento. Altere ou remova o seed de usuário antes de qualquer ambiente compartilhado ou de produção.

## ⚙️ Valores de configuração

Após criar o `.env` na etapa 2, ajuste seus valores quando necessário:

```env
DATABASE_URL=postgresql://skatesham:skatesham-github@localhost/skatesham
SECRET_KEY=change-this-in-production
DEBUG=false
ENVIRONMENT=development
```

O `DATABASE_URL` é usado pela API, Alembic e executor de seeds. No Docker, a conexão é apontada automaticamente para o serviço `db`.

## 🧭 Estrutura

```text
app/                 API e regras de domínio
db/migration/        configuração e revisões do Alembic
db/seed/             seeds versionados e executor
tests/               testes automatizados
Dockerfile           imagem da API
docker-compose.yml   API, PostgreSQL e Adminer
Makefile             comandos de desenvolvimento
```

## 🛣️ Endpoints

- `POST /api/v1/auth/login/`
- `POST /api/v1/auth/register/`
- `GET /api/v1/buyers/`, `POST /api/v1/buyers/`
- `GET /api/v1/cars/`, `POST /api/v1/cars/`
- `GET /api/v1/sales/`, `POST /api/v1/sales/`
- `GET /health`

## 📄 Licença

Distribuído sob a licença MIT. Consulte [LICENSE](LICENSE).
