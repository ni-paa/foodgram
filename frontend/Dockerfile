# build env
FROM node:21.7.1-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
ENV PUBLIC_URL=/
RUN npm run build
# Копируем файлы сборки в директорию, доступную через volume
RUN mkdir -p /static
RUN cp -r build/* /static/
CMD ["tail", "-f", "/dev/null"]
