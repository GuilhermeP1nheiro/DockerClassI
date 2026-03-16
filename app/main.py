from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.cache import (
    get_cached_usuarios,
    invalidate_usuarios_cache,
    redis_client,
    set_cached_usuarios,
)
from app.database import Base, engine, get_db

app = FastAPI(title="Padaria API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    # Cria automaticamente as tabelas no PostgreSQL ao subir a API.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck(db: Session = Depends(get_db)):
    status = {
        "api": "ok",
        "postgres": "ok",
        "redis": "ok",
    }

    try:
        db.execute(text("SELECT 1"))
    except Exception:
        status["postgres"] = "error"

    try:
        redis_client.ping()
    except Exception:
        status["redis"] = "error"

    overall_ok = all(value == "ok" for value in status.values())
    return {
        "status": "ok" if overall_ok else "degraded",
        "checks": status,
    }


@app.post("/usuarios", response_model=schemas.UsuarioResponse, status_code=201)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        criado = crud.create_usuario(db, usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email ja cadastrado")

    # Sempre invalida cache da listagem quando houver escrita.
    invalidate_usuarios_cache()
    return criado


@app.get("/usuarios", response_model=list[schemas.UsuarioResponse])
def list_usuarios(db: Session = Depends(get_db)):
    cached = get_cached_usuarios()
    if cached is not None:
        return cached

    usuarios = crud.get_usuarios(db)
    usuarios_as_dict = [
        schemas.UsuarioResponse.model_validate(usuario).model_dump() for usuario in usuarios
    ]
    set_cached_usuarios(usuarios_as_dict)
    return usuarios_as_dict


@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return usuario
