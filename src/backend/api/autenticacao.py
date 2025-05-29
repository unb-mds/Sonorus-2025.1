from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from sqlalchemy.orm import Session
from src.backend.database.db_connection import get_db
from src.backend.services.autenticacao_voz import processar_e_verificar_voz
from src.backend.services.business_logic import registrar_usuario, autenticar_usuario
from src.backend.models.modelos import UsuarioRegistro, UsuarioLogin

roteador_autenticacao = APIRouter()

@roteador_autenticacao.post("/registrar")
async def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    sucesso = registrar_usuario(usuario, db)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return {"mensagem": "Usuário registrado com sucesso"}

@roteador_autenticacao.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    autenticado = autenticar_usuario(username, password, db)
    if autenticado:
        from src.backend.services.business_logic import criar_token_acesso
        token = criar_token_acesso({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")