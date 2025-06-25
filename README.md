# 🔐 Sonorus

![Sonorus](src/frontend/public/sororus_menor.png)

![CI](https://github.com/unb-mds/Sonorus-2025.1/actions/workflows/ci.yml/badge.svg)

Sonorus é uma **API de reconhecimento biométrico por voz** integrada a um sistema de login tradicional, utilizando **SpeechBrain**, **FastAPI** e **PostgreSQL**. O usuário pode se registrar, autenticar com senha e validar sua identidade por biometria de voz. O sistema utiliza **Redis** para cache de embeddings, garantindo performance e escalabilidade.

---

## 📎 Links Úteis

- [Figma - Projeto (StoryMap)](https://www.figma.com/board/b3El7KviXHzQEFS7IuhGyo/Projeto-MDS--Copy-?node-id=0-1&t=bZuBbWs4QZgYPwbc-1)
- [Figma - Protótipo](https://www.figma.com/proto/QTXFDiqQfiVNi7GRcvbs1q/Tela-de-login?node-id=1-2&t=HCUUayChkonQImLr-1&starting-point-node-id=1%3A2)
- [GitHub Page](https://unb-mds.github.io/Sonorus-2025.1/)
- [Arquitetura](./docs/arquitetura_software/)
- [Requisitos](./docs/requisitos.md)

---

## 🧠 Tecnologias Utilizadas

- **Backend:** FastAPI, SQLAlchemy, SpeechBrain, Redis, JWT, bcrypt
- **Frontend:** ReactJS, CSS
- **Banco de Dados:** PostgreSQL
- **Cache:** Redis
- **DevOps:** Docker, Docker Compose

---

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
│   │   ├── src/
│   │   ├── public/
│   │   └── package.json
├── README.md
├── docs/
│   ├── arquitetura_software/
│   ├── atas/
│   └── estudos/
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example` fornecido.  
**Nunca suba seu arquivo `.env` para o repositório!**

Exemplo:

```
# Backend
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/sonorus
JWT_CHAVE_SECRETA=sua_chave_secreta_super_segura
JWT_ALGORITMO=HS256

# Redis (opcional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 🚀 Como Executar Localmente

### 1. Clone o repositório

```bash
git clone github.com/unb-mds/Sonorus-2025.1
cd Sonorus-2025.1
```
### 2. Instale as dependências

```bash
chmod +x Build.sh
./Build.sh
```

### 3. Inicie o projeto

```bash
chmod +x Main.sh
./Main.sh
```

### 4. (Opcional) Suba o Redis

```bash
redis-server
```

### 5. Acesse a aplicação

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Como Executar com Docker

### 1. Build e up dos containers

```bash
docker-compose up --build
```

### 2. Serviços disponíveis

- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **PostgreSQL:** localhost:5432 (usuário/senha conforme `.env`)
- **Redis:** localhost:6379

### 3. Parar os containers

```bash
docker-compose down
```

---

## 🔊 Como Usar

### ▶️ Registro de Usuário

### ▶️ Login

### ▶️ Registro de Voz

### ▶️ Autenticação por Voz

---

## 🧪 Modelo Usado

- ECAPA-TDNN do speechbrain/spkrec-ecapa-voxceleb

---

## 📂 Armazenamento

- Embeddings de voz são armazenados no campo `embedding` da tabela `usuario` no PostgreSQL.
- Embeddings recentes são cacheados no Redis para acelerar autenticações.

---

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
|Douglas Wilson       | [Dodeglinhass](https://github.com/Dodeglinhass) |
|Daniel Teles         | [dtdanielteles](https://github.com/dtdanielteles) |
|José Joaquim         | [Joaquim-SNeto](https://github.com/Joaquim-SNeto) |
|Luan Vinícius        | [luannvi](https://github.com/luannvi) |
|Matheus Lemes        | [matheuslemesam](https://github.com/matheuslemesam) |
|Paulo Henrique       | [Pauloswimming](https://github.com/Pauloswimming) |
|Paulo Nery           | [Pnery2004](https://github.com/Pnery2004) |
|Rafael Barbosa       | [rafaelbdmelo117](https://github.com/rafaelbdmelo117) |

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📬 Contato

Dúvidas ou sugestões? Abra uma issue ou entre em contato com os mantenedores do projeto.

---
