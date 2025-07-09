# Script de automação para instalação do Sonorus no Linux
# Certifique-se de que você tem permissões de administrador para executar este script (chmod +x Build.sh)
pip install python3-venv

python3 -m venv SonorusVenv

source SonorusVenv/bin/activate

pip install -r requirements.txt

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

REACT_APP_API_URL=http://localhost:8000/api

REACT_APP_DNS_API_URL=https://cloudflare-dns.com/dns-query
EOF

sudo apt install -y npm

cd src/frontend

rm -rf node_modules package-lock.json

npm install

npm install react-scripts@5.0.1 --save
