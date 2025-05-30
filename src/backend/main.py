# src/backend/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.database.db_connection import SessionLocal  # Importação atualizada!

app = FastAPI()

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    return {"status": "Conectado ao PostgreSQL!"}