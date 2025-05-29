from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from src.backend.database.db_connection import get_db
from src.backend.services.voz_service import registrar_embedding_voz, autenticar_por_voz
from src.backend.services.business_logic import obter_usuario_atual

roteador_autenticacao = APIRouter()

@roteador_autenticacao.post("/registrar-voz")
async def registrar_voz(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario = Depends(obter_usuario_atual)
):
    """
    Endpoint para registrar a voz do usuário (cadastro).
    O usuário deve falar: "Minha voz é minha senha" por 10 segundos.
    """
    print(f"Usuário: {usuario.email}, Arquivo: {arquivo.filename}")
    try:
        embedding = registrar_embedding_voz(usuario.id, arquivo, db)
        return {"mensagem": "Voz registrada com sucesso!", "embedding": embedding.tolist()}
    except Exception as e:
        print(f"Erro ao registrar voz: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao registrar voz: {e}")

@roteador_autenticacao.post("/autenticar-voz")
async def autenticar_voz(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario = Depends(obter_usuario_atual)
):
    """
    Endpoint para autenticação de 2 fatores por voz.
    O usuário deve estar logado (senha de texto) e falar a frase.
    """
    similaridade = autenticar_por_voz(usuario.id, arquivo, db)
    if similaridade > 0.8:
        return {"mensagem": "Autenticação por voz bem-sucedida", "pontuacao_similaridade": round(similaridade * 100, 2)}
    else:
        raise HTTPException(
            status_code=401,
            detail={"mensagem": "Autenticação por voz falhou", "pontuacao_similaridade": round(similaridade * 100, 2)}
        )