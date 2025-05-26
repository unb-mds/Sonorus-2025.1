# Imagem base oficial do Python
FROM python:3.11-slim-bookworm

# Atualiza os pacotes do sistema para corrigir vulnerabilidades
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos para o container
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o container
COPY . .

# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]