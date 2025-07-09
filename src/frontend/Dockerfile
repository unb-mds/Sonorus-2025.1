# Estágio 1: Build da aplicação React
FROM node:18-alpine as build

WORKDIR /app

# Copia os arquivos de manifesto de pacotes e instala as dependências
COPY package.json ./
# Se você tiver um package-lock.json, é bom copiá-lo também
# COPY package-lock.json ./
RUN npm install

# Copia o resto dos arquivos da aplicação
COPY . .

# Define a URL da API como um argumento de build
# O valor padrão será /api, que funcionará com o proxy reverso do Nginx
ARG REACT_APP_API_URL=/api
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Builda a aplicação para produção
RUN npm run build

# Estágio 2: Servir a aplicação com Nginx
FROM nginx:stable-alpine

# Copia os arquivos de build do estágio anterior para o diretório padrão do Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia a nova configuração do Nginx
COPY nginx.conf /etc/nginx/conf.d

# Expõe a porta 80
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
