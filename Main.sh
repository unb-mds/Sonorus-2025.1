# script para iniciar o backend e frontend do Sonorus no Linux
# verifique se deu as permissões de execução com: chmod +x Main.sh
# Certifique-se de não estar na Área de trabalho ou em diretórios com espaço, pois o script pode não funcionar corretamente.

sudo systemctl start redis-server

if [ -d "./SonorusVenv" ]; then
  source ./SonorusVenv/bin/activate
else
  echo "Ambiente virtual SonorusVenv não encontrado. Execute 'python3 -m venv SonorusVenv' e instale as dependências."
  exit 1
fi

gnome-terminal -- bash -c "cd $(pwd); uvicorn src.backend.main:app --reload; exec bash"

if [ -d "./src/frontend" ]; then
  gnome-terminal -- bash -c "cd $(pwd)/src/frontend; npm start; exec bash"
else
  echo "Diretório ./src/frontend não encontrado."
fi