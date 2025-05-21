from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import constr
from src.backend.services.autenticacao_voz import processar_e_verificar_voz
from src.backend.services.business_logic import register_user, login_user
from src.backend.models.modelos import UsuarioRegistro, UsuarioLogin

roteador_autenticacao = APIRouter()

# Endpoint para registro de usuário
@roteador_autenticacao.post("/registrar")
async def registrar(usuario: UsuarioRegistro):
    sucesso = registrar_usuario(usuario)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return {"mensagem": "Usuário registrado com sucesso"}

# Endpoint para login de usuário
@roteador_autenticacao.post("/login")
async def login(usuario: UsuarioLogin):
    autenticado = autenticar_usuario(usuario.email, usuario.senha)
    if autenticado:
        return {"mensagem": "Login realizado com sucesso"}
    else:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

# Endpoint para autenticação por voz
@roteador_autenticacao.post("/verificar-voz")
async def verificar_voz(login: str, arquivo: UploadFile = File(...)):
    """
    Endpoint para autenticação por voz.
    """
    try:
        pontuacao_similaridade = processar_e_verificar_voz(login, arquivo)
    except HTTPException as e:
        raise e

    # Verifica se a pontuação de similaridade é suficiente para autenticação
    if pontuacao_similaridade > 0.8:
        return {
            "mensagem": "Autenticação bem-sucedida",
            "pontuacao_similaridade": round(pontuacao_similaridade * 100, 2)
        }
    else:
        # Retorna erro 401 se a pontuação for insuficiente
        raise HTTPException(
            status_code=401,
            detail={
                "mensagem": "Autenticação falhou",
                "pontuacao_similaridade": round(pontuacao_similaridade * 100, 2)
            }
        )

"""
para testar o endpoint de autenticação por voz, siga os passos abaixo:

navegue até o repositório: cd /path/to/your/repo

instale as dependências: pip install -r requirements.txt

execute o servidor com o comando: uvicorn src.backend.main:app --reload

use o seguinte comando para testar o endpoint de verificação de voz:
curl -X POST "http://127.0.0.1:8000/auth/verify-voice"
-H "accept: application/json"
-H "Content-Type: multipart/form-data"
-F "email=user1"
-F "file=@path_to_audio.wav"

ou 

http://127.0.0.1:8000/docs
auth/verificar voz
try it out

"""
