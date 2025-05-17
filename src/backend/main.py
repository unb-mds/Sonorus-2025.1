from fastapi import FastAPI
from src.backend.api.autenticacao import roteador_autenticacao
from src.backend.database.database import initialize_db

app = FastAPI(title="Voice Biometrics API")

# Initialize database
initialize_db()

# Include authentication routes
app.include_router(roteador_autenticacao, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Welcome to the Voice Biometrics API"}