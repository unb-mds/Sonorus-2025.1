from pydantic import BaseModel

class UsuarioRegistro(BaseModel):
    nome: str
    sobrenome: str
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str