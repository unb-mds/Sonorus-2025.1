#!/bin/bash
# Script para iniciar o backend e frontend do Sonorus usando tmux

# Inicia o redis
sudo systemctl start redis-server

# Verifica e ativa o ambiente virtual
if [ -d "./SonorusVenv" ]; then
  source ./SonorusVenv/bin/activate
else
  echo "Ambiente virtual SonorusVenv não encontrado."
  exit 1
fi

# Nome da sessão tmux
SESSION_NAME="sonorus"

# Mata qualquer sessão tmux antiga com o mesmo nome para começar do zero
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Cria uma nova sessão tmux desanexada
echo "Iniciando sessão tmux '$SESSION_NAME'..."
tmux new-session -d -s $SESSION_NAME

# Janela 0: Inicia o Backend (uvicorn)
echo "Iniciando o Backend na janela 0..."
tmux send-keys -t $SESSION_NAME:0 "cd $(pwd) && uvicorn src.backend.main:app --host 0.0.0.0 --reload" C-m

# Cria uma nova janela para o Frontend
tmux new-window -t $SESSION_NAME:1

# Janela 1: Inicia o Frontend (npm start)
echo "Iniciando o Frontend na janela 1..."
tmux send-keys -t $SESSION_NAME:1 "cd $(pwd)/src/frontend && npm start" C-m

# Anexa à sessão tmux para você ver os processos
echo "Anexando à sessão. Pressione Ctrl+b e depois 'd' para desanexar."
tmux attach-session -t $SESSION_NAME
