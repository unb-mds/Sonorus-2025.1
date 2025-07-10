# Etapa 1: build dos arquivos estáticos (opcional para produção)
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Se quiser buildar para produção, descomente a linha abaixo:
# RUN npm run build

# Etapa 2: ambiente de desenvolvimento (npm start)
FROM node:18-alpine
WORKDIR /app
COPY --from=build /app /app
EXPOSE 3000
ENV PATH /app/node_modules/.bin:$PATH
CMD ["npm", "start"]