# 🔐 Voice Biometrics API

Este projeto implementa uma **API de reconhecimento biométrico por voz** integrada a um sistema de login tradicional, utilizando **SpeechBrain** e **FastAPI**. Agora, o fluxo está completo: o usuário pode se registrar, autenticar com senha e, em seguida, validar sua identidade por biometria de voz. O sistema utiliza **PostgreSQL** para persistência e **Redis** para cache de embeddings, garantindo performance e escalabilidade.

## 📎 Links Úteis

- [Figma - Projeto (StoryMap)](https://www.figma.com/board/b3El7KviXHzQEFS7IuhGyo/Projeto-MDS--Copy-?node-id=0-1&t=bZuBbWs4QZgYPwbc-1)
- [Figma - Protótipo](https://www.figma.com/proto/QTXFDiqQfiVNi7GRcvbs1q/Tela-de-login?node-id=1-2&t=HCUUayChkonQImLr-1&starting-point-node-id=1%3A2)
- [GitHub Page](https://unb-mds.github.io/Sonorus-2025.1/)
- [Arquitetura](./docs/arquitetura_software/)
- [Requisitos](./docs/requisitos.md)

## 🧠 Tecnologias Utilizadas

**Frontend**
- HTML, CSS, TailwindCSS, JavaScript, ReactJs

**Backend**
- Python, FastAPI, SpeechBrain, SQLAlchemy

**Banco de dados**
- PostgreSQL

**Cache**
- Redis

## 📁 Estrutura do Projeto

```
Biometria-Vocal-2025.1/
├── src
│   ├── backend/
│   │   ├── api/
│   │   ├── database/
│   │   ├── models/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── CSS/
│   │   ├── HTML/
│   │   └── JS/
├── README.md
├── docs/
│   ├── arquitetura_software/
│   ├── atas/
│   └── estudos/
└── .gitignore
```

## ⚙️ Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para armazenar configurações sensíveis e específicas do ambiente, como credenciais de banco de dados, chaves de API, diretórios de backup, entre outros.

Antes de rodar o projeto, crie um arquivo `.env` na raiz do repositório com base no arquivo `env.example` fornecido. Preencha os valores conforme o seu ambiente.

Exemplo de `.env`:

```
JWT_CHAVE_SECRETA=sua_chave
JWT_ALGORITMO=HS256
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/sonorus
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

**Nunca suba seu arquivo `.env` para o repositório!**  

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/unb-mds/Biometria-Vocal-2025.1.git
   cd Biometria-Vocal-2025.1
   ```

2. **Crie e configure o arquivo `.env` na raiz do projeto.**

3. **Navegue até o diretório do backend:**
   ```bash
   cd src/backend
   ```

4. **Crie e ative um ambiente virtual:**
   - No Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - No Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

5. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Inicie o Redis (se ainda não estiver rodando):**
   ```bash
   redis-server
   ```

7. **Inicie o servidor:**
   ```bash
   uvicorn src.backend.main:app --reload
   ```

8. **Acesse a API:**
   - Documentação Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Documentação Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🔊 Como Usar

### ▶️ Registro de Usuário

- Envie uma requisição para `/registrar` com nome, email e senha.

### ▶️ Login

- Envie uma requisição para `/login` com email e senha para receber o token JWT.

### ▶️ Registro de Voz

- Após login, envie um arquivo `.wav` (mono, 16kHz, 16 bits) para `/registrar-voz` com o token JWT no header.
- Use o script `src/backend/utils/gravar_wav.py` para gravar o áudio no formato correto.

### ▶️ Autenticação por Voz

- Envie um arquivo `.wav` para `/autenticar-voz` com o token JWT no header.
- O sistema compara o embedding do áudio enviado com o embedding salvo.

## 🧪 Modelo Usado

- ECAPA-TDNN do speechbrain/spkrec-ecapa-voxceleb

## 📂 Armazenamento

- Embeddings de voz são armazenados no campo `embedding` da tabela `usuario` no PostgreSQL.
- Embeddings recentes são cacheados no Redis para acelerar autenticações.

## 🛠️ Scripts Úteis

- **Gravação de áudio:**  
  Use o script `src/backend/utils/gravar_wav.py` para gravar áudios compatíveis com o modelo.

---

## 📚 Documentação Complementar

- [docs/arquitetura_software/Fluxo-Login.md](docs/arquitetura_software/Fluxo-Login.md): Detalha o fluxo de autenticação biométrica.
- [docs/arquitetura_software/Fluxograma-Cadastro.md](docs/arquitetura_software/Fluxograma-Cadastro.md): Explica o fluxo de cadastro com biometria de voz.
- [docs/Database/import.md](docs/Database/import.md): Estrutura do banco de dados e tabelas utilizadas.
- [docs/requisitos.md](docs/requisitos.md): Requisitos funcionais e não funcionais do sistema.

---

## 🧑‍💻 Contribuição

Veja o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para saber como contribuir.

---

## 🛡️ Segurança

- Senhas são armazenadas com hash (bcrypt).
- Dados biométricos são protegidos e nunca expostos diretamente.
- Políticas de bloqueio após múltiplas tentativas de autenticação falha.

---

## 👥 Contribuidores

| Nome                | GitHub        |
|---------------------|-------------------------|
|Douglas Wilson       | [Dodgelinhass](https://github.com/Dodgelinhass) |
|Daniel Teles         | [dtdanielteles](https://github.com/dtdanielteles) |
|José Joaquim         | [Joaquim-SNeto](https://github.com/Joaquim-SNeto) |
|Luan Vinícius        | [luannvi](https://github.com/luannvi) |
|Matheus Lemes        | [matheuslemesam](https://github.com/matheuslemesam) |
|Paulo Henrique       | [Pauloswimming](https://github.com/Pauloswimming) |
|Paulo Nery           | [Pnery2004](https://github.com/Pnery2004) |
|Rafael Barbosa       | [rafaelbdmelo117](https://github.com/rafaelbdmelo117) |