# backup_automatico/backup.py
import os
import subprocess
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configurações
DB_NAME = "biometria_vocal"
DB_USER = "postgres"  # Ou seu usuário do PostgreSQL
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "backup_automatico")
DRIVE_FOLDER_ID = "SEU_ID_DA_PASTA_NO_DRIVE"
SERVICE_ACCOUNT_FILE = r"C:\caminho\para\credenciais.json"  # Caminho completo no Windows

# Criar nome do arquivo com data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.dump")

# Comando pg_dump para Windows
cmd = f'pg_dump -U {DB_USER} -d {DB_NAME} -F c -b -v -f "{backup_file}"'

# Executar comando
try:
    subprocess.run(cmd, shell=True, check=True)
    print(f"Backup criado: {backup_file}")
except subprocess.CalledProcessError as e:
    print(f"Erro no backup: {e}")
    exit(1)

# Upload para Google Drive
try:
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
        'name': os.path.basename(backup_file),
        'parents': [DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(backup_file)
    
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print("Backup enviado para Google Drive com sucesso!")
except Exception as e:
    print(f"Erro no upload: {e}")