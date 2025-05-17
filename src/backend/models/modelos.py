from pydantic import BaseModel

class UsuarioRegistro(BaseModel):
    login: str 
    senha: str
    primeiro_nome: str
    ultimo_nome: str

class UsuarioLogin(BaseModel):
    login: str  
    senha: str