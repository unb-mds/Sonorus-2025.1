import logging
import dns.resolver
from fastapi import APIRouter, HTTPException, Depends, Form
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
    # Verificação se o usuário já existe
    sucesso = registrar_usuario(usuario, db)
    if not sucesso:
        logger.info(f"Tentativa de registro falhou para email: {usuario.email} (usuário já existe)")
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # Validação do domínio do e-mail
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
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    autenticado = autenticar_usuario(email, password, db)
    if not autenticado:
        logger.info(f"Tentativa de login falhou para email: {email}")
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    logger.info(f"Login de senha bem-sucedido para email: {email}")
    pre_auth_token = criar_token_temporario({"sub": email, "acao": "autenticar_voz"})
    return {
        "mensagem": "Senha correta. Autentique-se por voz para concluir o login.",
        "pre_auth_token": pre_auth_token
    }

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

        usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or usuario.senha != password:
        logger.info(f"Tentativa de login falhou para email: {email}")
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    logger.info(f"Login de senha bem-sucedido para email: {email}")
    access_token = criar_token_temporario({"sub": usuario.email})
    return {
        "mensagem": "Login realizado com sucesso",
        "access_token": access_token
        }