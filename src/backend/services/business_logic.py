import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.backend.database.db_connection import get_db
from src.backend.models.modelos import UsuarioRegistro, UsuarioLogin
from src.backend.models.sqlalchemy import Usuario 

load_dotenv()

CHAVE_SECRETA = os.getenv("JWT_CHAVE_SECRETA")
ALGORITMO = os.getenv("JWT_ALGORITMO")

if not CHAVE_SECRETA or not ALGORITMO:
    raise RuntimeError("As variáveis de ambiente JWT_CHAVE_SECRETA e JWT_ALGORITMO devem estar definidas!")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def registrar_usuario(usuario: UsuarioRegistro, db: Session):
    if db.query(Usuario).filter_by(email=usuario.email).first():
        return False
    usuario_novo = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=pwd_context.hash(usuario.senha),
        embedding=[0.0] 
    )
    db.add(usuario_novo)
    db.commit()
    db.refresh(usuario_novo)
    return True

def autenticar_usuario(email: str, senha: str, db: Session):
    usuario = db.query(Usuario).filter_by(email=email).first()
    if not usuario or not pwd_context.verify(senha, usuario.senha):
        return False
    return True

def criar_token_acesso(dados: dict):
    from datetime import datetime, timedelta
    dados_para_codificar = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=60)
    dados_para_codificar.update({"exp": expira})
    token_jwt = jwt.encode(dados_para_codificar, CHAVE_SECRETA, algorithm=ALGORITMO)
    return token_jwt

def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    excecao_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        email: str = payload.get("sub")
        if email is None:
            raise excecao_credenciais
    except JWTError:
        raise excecao_credenciais
    usuario = db.query(Usuario).filter_by(email=email).first()  # <-- corrigido aqui
    if usuario is None:
        raise excecao_credenciais
    return usuario