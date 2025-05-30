import logging
from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from src.backend.database.db_connection import get_db
from src.backend.services.business_logic import registrar_usuario, autenticar_usuario, criar_token_temporario
from src.backend.models.modelos import UsuarioRegistro

logger = logging.getLogger("autenticacao_api")

roteador_autenticacao = APIRouter()

@roteador_autenticacao.post("/registrar")
async def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    sucesso = registrar_usuario(usuario, db)
    if not sucesso:
        logger.info(f"Tentativa de registro falhou para email: {usuario.email} (usuário já existe)")
        raise HTTPException(status_code=400, detail="Usuário já existe")
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