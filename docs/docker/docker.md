
# 🐳 Documentação Docker

## 📦 Dockerfile

O **Dockerfile** é um arquivo usado para criar uma imagem de container. Ele define os passos, dependências e configurações necessárias para a aplicação rodar dentro de um container.

### 🔧 Principais instruções:

- **FROM** – Define a imagem base (ex.: `python:3.10-slim`).
- **WORKDIR** – Define o diretório de trabalho dentro do container.
- **COPY** – Copia arquivos do projeto para dentro do container.
- **RUN** – Executa comandos no momento da construção da imagem (ex.: instalar dependências).
- **EXPOSE** – Documenta a porta que o container utilizará (não faz o mapeamento externo).
- **CMD** – Define o comando padrão a ser executado quando o container iniciar.

### 🔍 Exemplo de Dockerfile:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 🛠️ docker-compose.yml

O **docker-compose.yml** permite definir, configurar e rodar múltiplos containers como serviços, utilizando um único arquivo.

### 🚩 Principais funcionalidades:

- Gerencia múltiplos containers (ex.: aplicação, banco de dados, cache).
- Define redes, volumes e dependências entre serviços.
- Simplifica o processo de inicialização dos containers.

### 🔍 Estrutura comum:

- **version:** Define a versão do compose.
- **services:** Lista de containers.
- **build:** Instruções para construir a imagem a partir de um Dockerfile.
- **image:** Usa uma imagem pronta (ex.: `postgres:15`).
- **ports:** Faz o mapeamento de portas (ex.: `"5000:5000"`).
- **volumes:** Cria volumes persistentes ou compartilha diretórios locais.
- **environment:** Define variáveis de ambiente.
- **depends_on:** Define a ordem de inicialização dos containers.

### 🔧 Exemplo de docker-compose.yml:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: database
    ports:
      - "5432:5432"

volumes:
  postgres-data:
```

---

## 🚫 .dockerignore

O arquivo **.dockerignore** define quais arquivos e pastas serão ignorados no processo de construção da imagem Docker.

### 🎯 Finalidade:

- Reduzir o tamanho da imagem.
- Melhorar a performance do build.
- Evitar que arquivos sensíveis, desnecessários ou de desenvolvimento sejam copiados para o container.

### 🔧 Exemplos comuns de itens ignorados:

```
__pycache__/
*.pyc
*.pyo
*.log
*.env
.git
node_modules
dist
build
```

---
