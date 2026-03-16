from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    # Permite retornar objetos ORM direto do SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)
