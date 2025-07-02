from src.backend.database.db_connection import SessionLocal
from src.backend.models.sqlalchemy import Usuario

def excluir_todos_usuarios():
    db = SessionLocal()
    try:
        db.query(Usuario).delete()
        db.commit()
        print("Todos os usuários foram removidos.")
    finally:
        db.close()

if __name__ == "__main__":
    excluir_todos_usuarios()

# rodar na raiz com: python3 -m src.backend.utils.excluirUsuariosPSQL