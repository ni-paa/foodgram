## Запуск проекта

1. Перейдите в папку `infra`:
   ```
   cd infra
   ```

2. Запустите проект с помощью Docker Compose:
   ```
   docker-compose up --build
   ```

   Эта команда соберет и запустит все необходимые контейнеры:
   - `db` - база данных PostgreSQL
   - `backend` - Django backend API
   - `frontend` - сборка React frontend
   - `nginx` - веб-сервер и прокси

3. После запуска проект будет доступен по адресу:
   - **Frontend**: http://localhost
   - **API документация**: http://localhost/api/docs/

## Структура проекта

- `backend/` - Django REST API
- `frontend/` - React приложение
- `infra/` - конфигурация Docker
- `docs/` - OpenAPI спецификация
- `data/` - данные для загрузки (ингредиенты)

## API endpoints

Полная спецификация API доступна в `docs/openapi-schema.yml` и через интерфейс ReDoc по адресу http://localhost/api/docs/.
