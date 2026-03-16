# API de Estudo: FastAPI + PostgreSQL + Redis + Docker Compose

Projeto simples e didatico para estudar uma API REST em Python com cache e banco relacional.

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Docker e Docker Compose

## Estrutura

```text
.
|- app/
|  |- __init__.py
|  |- main.py
|  |- database.py
|  |- models.py
|  |- schemas.py
|  |- crud.py
|  |- cache.py
|- Dockerfile
|- docker-compose.yml
|- requirements.txt
|- .env.example
```

## Servicos no `docker-compose.yml`

- `api`: API FastAPI (porta `8000:8000`)
- `postgres`: PostgreSQL com volume persistente (porta `5432:5432`)
- `redis`: Redis para cache (porta `6379:6379`)

## Como subir o projeto

1. Criar o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

1. Subir os containers:

```bash
docker compose up --build
```

1. Acessar a API:

- API: `http://localhost:8000`
- Docs Swagger: `http://localhost:8000/docs`

## Como derrubar os containers

```bash
docker compose down
```

Para derrubar e remover volumes (apaga dados do PostgreSQL):

```bash
docker compose down -v
```

## Rotas da API

- `GET /health`
- `POST /usuarios`
- `GET /usuarios`
- `GET /usuarios/{id}`

## Regras de cache no `GET /usuarios`

- Primeiro verifica se existe cache no Redis.
- Se existir, retorna do Redis.
- Se nao existir, busca no PostgreSQL e salva no Redis por `60` segundos.
- Ao criar usuario (`POST /usuarios`), o cache da listagem e invalidado.

## Exemplos de `curl`

### Healthcheck

```bash
curl -X GET http://localhost:8000/health
```

### Criar usuario

```bash
curl -X POST http://localhost:8000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome":"Ana","email":"ana@example.com"}'
```

### Listar usuarios

```bash
curl -X GET http://localhost:8000/usuarios
```

### Buscar usuario por id

```bash
curl -X GET http://localhost:8000/usuarios/1
```

## Observacoes

- As tabelas sao criadas automaticamente no startup da API via SQLAlchemy.
- O volume `postgres_data` garante persistencia dos dados do PostgreSQL.
