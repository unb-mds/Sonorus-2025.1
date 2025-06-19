import logging
import dns.resolver
from fastapi import APIRouter, HTTPException, Depends, Form, Response, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.backend.database.db_connection import get_db
from src.backend.models.sqlalchemy import Usuario
from src.backend.services.business_logic import registrar_usuario, autenticar_usuario, criar_token_temporario
from src.backend.models.modelos import UsuarioRegistro

logger = logging.getLogger("autenticacao_api")

roteador_autenticacao = APIRouter()

class EmailRequest(BaseModel):
    email: str    

@roteador_autenticacao.post("/registrar")
async def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    sucesso = registrar_usuario(usuario, db)
    if not sucesso:
        logger.info(f"Tentativa de registro falhou para email: {usuario.email} (usuário já existe)")
        raise HTTPException(status_code=400, detail="Usuário já existe")
    try:
        dominio = usuario.email.split('@')[1]
    except IndexError:
        raise HTTPException(status_code=400, detail="Formato de e-mail inválido")
    if not dominio_tem_mx(dominio):
        logger.info(f"Registro com domínio de e-mail inválido: {usuario.email}")
        raise HTTPException(status_code=400, detail="Domínio de e-mail inexistente ou inválido")
    logger.info(f"Usuário registrado com sucesso: {usuario.email}")
    pre_auth_token = criar_token_temporario({"sub": usuario.email, "acao": "registrar_voz"})
    return {
        "mensagem": "Usuário registrado. Cadastre sua voz para concluir o registro.",
        "pre_auth_token": pre_auth_token
    }

@roteador_autenticacao.post("/login")
async def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    autenticado = autenticar_usuario(email, password, db)
    if not autenticado:
        logger.info(f"Tentativa de login falhou para email: {email}")
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    logger.info(f"Login de senha bem-sucedido para email: {email}")
    # Gera o JWT real - ajuste conforme sua lógica
    jwt_token = criar_token_temporario({"sub": email, "acao": "autenticar_voz"})
    # Define o cookie HttpOnly
    response = JSONResponse(content={"mensagem": "Login realizado com sucesso."})
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,  # True em produção (HTTPS)
        samesite="lax",
        max_age=60*60*24,
        path="/"
    )
    return response

def dominio_tem_mx(domain: str) -> bool:
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False

@roteador_autenticacao.post("/check-email")
def check_email(request: EmailRequest, db: Session = Depends(get_db)):
    email = request.email
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado no sistema")
    try:
        dominio = email.split('@')[1]
    except IndexError:
        raise HTTPException(status_code=400, detail="Formato de e-mail inválido")
    if not dominio_tem_mx(dominio):
        raise HTTPException(status_code=400, detail="Domínio de e-mail inválido")
    return {"mensagem": "E-mail válido e disponível"}

# Exemplo de proteção de rota
from fastapi import Depends

def get_jwt_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado")
    return token

@roteador_autenticacao.get("/rota-protegida")
def rota_protegida(token: str = Depends(get_jwt_from_cookie)):
    # Decodifique e valide o token normalmente aqui!
    return {"mensagem": "Acesso autorizado!"}
    
