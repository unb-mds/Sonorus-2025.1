import logging
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Header
from sqlalchemy.orm import Session
from src.backend.database.db_connection import get_db
from src.backend.services.voz_service import registrar_embedding_voz, autenticar_por_voz
from src.backend.services.business_logic import validar_token_temporario, criar_token_acesso

logger = logging.getLogger("voz_api")

roteador_autenticacao = APIRouter()

@roteador_autenticacao.post("/registrar-voz")
async def registrar_voz(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    """
    Endpoint para registrar a voz do usuário (cadastro).
    O usuário deve falar: "Minha voz é minha senha" por 10 segundos.
    """
    if not authorization.startswith("Bearer "):
        logger.info("Tentativa de registro de voz sem token temporário.")
        raise HTTPException(status_code=401, detail="Token temporário ausente")
    token = authorization.split(" ")[1]
    usuario = validar_token_temporario(token, "registrar_voz", db)
    if not usuario:
        logger.info("Token temporário inválido ou ação não permitida no registro de voz.")
        raise HTTPException(status_code=401, detail="Token temporário inválido ou ação não permitida")
    try:
        embedding = registrar_embedding_voz(usuario.id, arquivo, db)
        logger.info(f"Voz registrada com sucesso para usuário: {usuario.email}")
        return {"mensagem": "Voz registrada com sucesso!", "embedding": embedding.tolist()}
    except Exception as e:
        logger.exception(f"Erro ao registrar voz para usuário {usuario.email}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao registrar voz: {e}")

@roteador_autenticacao.post("/autenticar-voz")
async def autenticar_voz(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    """
    Endpoint para autenticação de 2 fatores por voz.
    O usuário deve estar logado (senha de texto) e falar a frase.
    """
    if not authorization.startswith("Bearer "):
        logger.info("Tentativa de autenticação de voz sem token temporário.")
        raise HTTPException(status_code=401, detail="Token temporário ausente")
    token = authorization.split(" ")[1]
    usuario = validar_token_temporario(token, "autenticar_voz", db)
    if not usuario:
        logger.info("Token temporário inválido ou ação não permitida na autenticação de voz.")
        raise HTTPException(status_code=401, detail="Token temporário inválido ou ação não permitida")
    
    # Chama a função que compara o áudio recebido com o embedding salvo
    similaridade = autenticar_por_voz(usuario.id, arquivo, db)
    LIMIAR = 0.9  # Defina o limiar de similaridade (ajuste conforme necessário)
    if similaridade > LIMIAR:
        access_token = criar_token_acesso({"sub": usuario.email})
        logger.info(f"Autenticação por voz bem-sucedida para usuário: {usuario.email} (similaridade: {similaridade})")
        return {
            "mensagem": "Autenticação por voz bem-sucedida",
            "pontuacao_similaridade": round(similaridade * 100, 2),
            "access_token": access_token
        }
    else:
        logger.info(f"Autenticação por voz falhou para usuário: {usuario.email} (similaridade: {similaridade})")
        raise HTTPException(
            status_code=401,
            detail={"mensagem": "Autenticação por voz falhou", "pontuacao_similaridade": round(similaridade * 100, 2)}
        )