import os
from fastapi import Depends, HTTPException, status, Request
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
        sobrenome=usuario.sobrenome,
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

def criar_token_temporario(dados: dict, minutos_expiracao: int = 10):
    """
    Cria um token JWT temporário, usado para registrar ou autenticar voz.
    Por padrão, expira em 10 minutos.
    """
    from datetime import datetime, timedelta
    dados_para_codificar = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=minutos_expiracao)
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
    usuario = db.query(Usuario).filter_by(email=email).first()
    if usuario is None:
        raise excecao_credenciais
    return usuario

def validar_token_temporario(token: str, acao_esperada: str, db: Session):
    """
    Valida um token JWT temporário e verifica se a ação esperada corresponde.
    Retorna o usuário se válido, ou None caso contrário.
    """
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        email = payload.get("sub")
        acao = payload.get("acao")
        if not email or acao != acao_esperada:
            return None
        usuario = db.query(Usuario).filter_by(email=email).first()
        if not usuario:
            return None
        return usuario
    except JWTError:
        return None

def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def get_jwt_from_cookie(request: Request):
    # Primeiro tenta pegar do cookie
    token = request.cookies.get("access_token")
    # Se não achar, tenta pegar do header Authorization
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
    if not token:
        return None
    return token