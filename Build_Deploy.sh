# Script de automação para instalação do Sonorus no Linux
# Certifique-se de que você tem permissões de administrador para executar este script (chmod +x Build.sh)

apt-get update && apt-get install -y build-essential

sudo apt-get install -y python3-dev

apt install python3-venv

python3 -m venv SonorusVenv

source SonorusVenv/bin/activate

mkdir -p ~/pip_temp

TMPDIR=~/pip_temp pip install -r requirements.txt

sudo mkdir -p pretrained_models/ecapa
sudo chown $USER:$USER pretrained_models/ecapa

sudo apt install -y postgresql postgresql-contrib

sudo apt-get install ffmpeg

sudo apt-get install -y redis-server

sudo systemctl enable redis-server

sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'MDS';" # troque MDS pela senha que você deseja

sudo -u postgres psql -c "CREATE DATABASE sonorus OWNER postgres;" # troque sonorus pelo nome do banco de dados que você deseja

sudo -u postgres psql -d sonorus -f src/backend/database/scripts/create_tables.sql

cat > .env <<EOF
DATABASE_URL=postgresql://postgres:MDS@localhost:5432/sonorus #troque MDS pela senha que você definiu e sonorus pelo nome do banco de dados que você criou
JWT_CHAVE_SECRETA=$(openssl rand -base64 32)
JWT_ALGORITMO=HS256

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

REACT_APP_API_URL=http://129.212.188.212:8000/api # Altere para o IP do seu servidor ou localhost se estiver rodando localmente

REACT_APP_DNS_API_URL=https://cloudflare-dns.com/dns-query
EOF

sudo apt install -y npm

cd src/frontend

rm -rf node_modules package-lock.json

npm install

npm install react-scripts@5.0.1 --save
