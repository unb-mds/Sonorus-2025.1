from src.backend.database.db_connection import SessionLocal
from src.backend.models.sqlalchemy import Usuario

db = SessionLocal()
db.query(Usuario).delete()
db.commit()
db.close()
print("Todos os usuários foram removidos.")

# rodar na raiz com: python3 -m src.backend.utils.excluirUsuariosPSQL