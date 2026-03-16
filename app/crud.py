from sqlalchemy.orm import Session

from app import models, schemas


def create_usuario(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    novo_usuario = models.Usuario(nome=usuario.nome, email=usuario.email)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


def get_usuarios(db: Session) -> list[models.Usuario]:
    return db.query(models.Usuario).order_by(models.Usuario.id).all()


def get_usuario_by_id(db: Session, usuario_id: int) -> models.Usuario | None:
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
