# backup_automatico/backup.py
import os
import subprocess  # ATENÇÃO: O uso do módulo subprocess pode trazer riscos de segurança. Evite executar comandos externos com dados não confiáveis.
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()

# Configurações
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
BACKUP_DIR = os.getenv("BACKUP_DIR")

# Criar nome do arquivo com data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.dump")

# Comando pg_dump para Linux (evite shell=True, passe argumentos como lista)
cmd = [
    "pg_dump",
    "-U", DB_USER,
    "-d", DB_NAME,
    "-F", "c",
    "-b",
    "-v",
    "-f", backup_file
]

# Executar comando de forma segura (sem shell=True)
try:
    # ATENÇÃO: subprocess pode ser perigoso se receber dados não confiáveis.
    subprocess.run(cmd, check=True)
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
