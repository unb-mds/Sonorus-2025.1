# Testes de Integração Backend + Frontend — Sonorus

## Objetivo

Validar a integração real entre o backend (FastAPI + PostgreSQL + Redis) e o frontend (ReactJS), garantindo que os principais fluxos do usuário funcionam de ponta a ponta no ambiente local.

---

## Ambiente de Teste

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Redis
- **Frontend:** ReactJS
- **Execução:** Local, conforme instruções do [README.md](../../README.md) utilizando os scripts em Shell
- **Banco de Dados:** PostgreSQL (sonorus_test)
- **Cache:** Redis local

---

## Passos Realizados

1. **Clonagem e Instalação**
   - Clonei o repositório e instalei as dependências com `./Build.sh`.

2. **Configuração das Variáveis de Ambiente**
   - Configurei o `.env` com as URLs corretas para backend, banco e Redis.

3. **Inicialização dos Serviços**
   - Iniciei os serviços do backend, frontend e redis-server com o `./Main.sh`.

4. **Execução dos Fluxos de Teste**
   - Acesseio o frontend em `http://localhost:3000`.
   - Realizei o cadastro de um novo usuário (nome, sobrenome, email, senha).
   - Realizei o cadastro de voz (upload de áudio pelo frontend).
   - Autentiquei com email/senha e depois por voz.
   - Testei fluxos de erro: login inválido, áudio inválido, usuário inexistente.
   - Validei feedbacks visuais e mensagens do frontend.

5. **Verificação no Backend**
   - Conferi logs do backend para garantir que as requisições chegaram e foram processadas corretamente.
   - Verifiquei a persistência dos dados no banco PostgreSQL.
   - Testei o cache de embeddings no Redis.

## Bugs descobertos:

### Backend:

1. **Bug: Fluxo de usuário**
    - Em casos em que o usuário consegue se cadastrar por texto mas ao cadastrar a voz dá erro, notei que ele não consegue se recadastrar, consta que o email já está cadastrado.

### Frontend:

1. **Bug: Falta de informações ao gravar e autenticar a voz**
    - Em casos em que o usuário está cadastrando ou autenticando a voz notei que não tem instruções para o botão do microfone para ele iniciar e terminar a gravação.

2. **Bug: Falta de informações ao autenticar a voz**
    - Em casos em que o usuário está autenticando a voz notei que quando a autenticação não é permitida o frontend aparece que houve um erro na autenticação quando deveria aparecer autenticação não autorizada ou algo semelhante.

