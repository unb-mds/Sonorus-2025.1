# 🔐 Voice Biometrics API

Este projeto implementa uma **API de reconhecimento biométrico por voz** em um modelo de login já existente utilizando **SpeechBrain** e **FastAPI**. A API permite que usuários registrem sua voz e, posteriormente, sejam autenticados com base em suas características vocais únicas.

## 📎Links Úteis

- [Figma - Projeto (StoryMap)](https://www.figma.com/board/b3El7KviXHzQEFS7IuhGyo/Projeto-MDS--Copy-?node-id=0-1&t=bZuBbWs4QZgYPwbc-1)
- [Figma - Protótipo](https://www.figma.com/proto/QTXFDiqQfiVNi7GRcvbs1q/Tela-de-login?node-id=1-2&t=HCUUayChkonQImLr-1&starting-point-node-id=1%3A2)
- [GitHub Page](https://unb-mds.github.io/Sonorus-2025.1/)
- [Arquitetura](./docs/arquitetura_software/)
- [Requisitos](./docs/requisitos.md)

## 🧠 Tecnologias Utilizadas

**Frontend**
    - HTML
    - CSS
    - TailwindCSS
    - JavaScript
    - ReactJs

**Backend**
    - Python
    - SpeechBrain
    - FastAPI

**Banco de dados**
    - Oracle Database

## 📁 Estrutura do Projeto

```
Biometria-Vocal-2025.1/
├── src
    ├── backend/
        ├── api/
        ├── database/
        ├── models/
        ├── services/
        ├── utils/
        ├── main.py
        └── requirements.txt
    ├── frontend/
        ├── CSS/
        ├── HTML/
        └── JS/
├── LICENSE
├── README.md
├── docs/
    ├── arquitetura_software/
    ├── atas/
    └── estudos/
└── .gitignore
```

## ⚙️ Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para armazenar configurações sensíveis e específicas do ambiente, como credenciais de banco de dados, chaves de API, diretórios de backup, entre outros.

Antes de rodar o projeto, crie um arquivo `.env` na raiz do repositório com base no arquivo `env.example` fornecido. Preencha os valores conforme o seu ambiente.

Exemplo de `env.example`:

   DB_NAME=biometria_vocal
   DB_USER=postgres
   BACKUP_DIR=/caminho/para/backups
   DRIVE_FOLDER_ID=SEU_ID_DA_PASTA_NO_DRIVE
   SERVICE_ACCOUNT_FILE=/etc/backup_credentials/credenciais.json

**Nunca suba seu arquivo `.env` para o repositório!**  
O arquivo `.env` está listado no `.gitignore` para evitar o versionamento de informações sensíveis.

## 🚀 Como Executar
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/unb-mds/Biometria-Vocal-2025.1.git
   cd Biometria-Vocal-2025.1
   ```

2. **Crie um .env na raiz do projeto**
   touch .env
   Edite o arquivo .env com suas configurações.

3. **Navegue até o diretório do backend:**
   ```bash
   cd src/backend
   ```

4. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   - No Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - No Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

5. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Inicie o servidor:**
   ```bash
   uvicorn main:app --reload
   ```

7. **Acesse a API:**
   - Acesse a documentação interativa no navegador em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Ou veja a documentação alternativa em: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

8. **Encerrar o servidor:**
   - Pressione `Ctrl + C` no terminal para parar o servidor.


## 🔊 Como Usar


### ▶️ Registro


### ✅ Verificação


## 🧪 Modelo Usado
ECAPA-TDNN do speechbrain/spkrec-ecapa-voxceleb

## 📂 Armazenamento

## Contribuidores

| Nome                | GitHub        |
|---------------------|-------------------------|
|Douglas Wilson       | [Dodeglinhass](https://github.com/Dodeglinhass) |
|Daniel Teles         | [dtdanielteles](https://github.com/dtdanielteles) |
|José Joaquim         | [Joaquim-SNeto](https://github.com/Joaquim-SNeto) |
|Luan Vinícius        | [luannvi](https://github.com/luannvi) |
|Matheus Lemes        | [matheuslemesam](https://github.com/matheuslemesam) |
|Paulo Henrique       | [Pauloswimming](https://github.com/Pauloswimming) |
|Paulo Nery           | [Pnery2004](https://github.com/Pnery2004) |
|Rafael Barbosa       | [rafaelbdmelo117](https://github.com/rafaelbdmelo117) |
