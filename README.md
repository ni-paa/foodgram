# Foodgram - «Продуктовый помощник»
[![Foodgram CI/CD](https://github.com/ni-paa/foodgram/actions/workflows/main.yml/badge.svg)](https://github.com/ni-paa/foodgram/actions/workflows/main.yml)
[![Python](https://img.shields.io/badge/Python-3.9-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-3.2-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST](https://img.shields.io/badge/Django%20REST-3.12.4-ff1709.svg?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Nginx](https://img.shields.io/badge/Nginx-1.21-009639.svg?logo=nginx&logoColor=white)](https://nginx.org/ru/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1-499848.svg?logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?logo=githubactions&logoColor=white)](https://docs.github.com/actions)

**Foodgram** — это онлайн-сервис для публикации рецептов. Пользователи могут создавать свои собственные рецепты, просматривать рецепты других авторов, подписываться на любимых кулинаров, добавлять понравившиеся рецепты в «Избранное» и формировать список покупок для выбранных рецептов.

Сайт запущенного проекта доступен по адресу: [https://food.vsdb.ru/](https://food.vsdb.ru/)

## 📚 Документация API

После запуска проекта полная документация API доступна по адресам:

* **Swagger UI** (интерактивная документация с тестированием): [https://food.vsdb.ru/api/docs/](https://food.vsdb.ru/api/docs/)
* **ReDoc** (альтернативный вид документации): [https://food.vsdb.ru/api/redoc/](https://food.vsdb.ru/api/redoc/)


### 🔍 В документации вы найдете:
- Полное описание всех эндпоинтов API
- Параметры запросов и форматы ответов
- Примеры кода для всех операций
- Возможность тестирования API прямо в браузере

### 🔐 Аутентификация
Для доступа к защищенным эндпоинтам необходимо:
1. Зарегистрировать пользователя: `POST /api/users/`
2. Получить токен аутентификации: `POST /api/auth/token/login/`
3. Добавить токен в заголовки запросов: `Authorization: Token ваш_токен`

### 🎯 Основные эндпоинты:
- **Пользователи:** `/api/users/`, `/api/users/{id}/subscribe/`
- **Рецепты:** `/api/recipes/`, `/api/recipes/{id}/favorite/`, `/api/recipes/{id}/get-link/`
- **Списки:** `/api/users/subscriptions/`, `/api/recipes/download_shopping_cart/`
- **Справочники:** `/api/tags/`, `/api/ingredients/`

## 🚀 Функциональность

### Для всех пользователей:
* **Просмотр рецептов:** Доступ к общей ленте всех рецептов.
* **Просмотр отдельных рецептов:** Детальная страница с полным описанием, ингредиентами и шагами приготовления.
* **Фильтрация:** Фильтрация рецептов по тегам (например, "Завтрак", "Обед", "Ужин").

### Для авторизованных пользователей:
* **Создание и управление рецептами:** Возможность публиковать, редактировать и удалять свои рецепты.
* **Избранное:** Добавление рецептов в избранное и их просмотр в отдельном разделе.
* **Список покупок:** Добавление ингредиентов из рецептов в персональный список покупок.
    * Скачивание списка в формате PDF.
* **Подписки:** Подписка на публикации других авторов и просмотр их рецептов в своей ленте.

### Административная панель:
* Полный контроль над пользователями, рецептами, ингредиентами и тегами через стандартную админ-панель Django.

---

## 🛠 Технологический стек

* **Backend:** Python 3.9, Django 3.2, Django REST Framework 3.12.4
* **База данных:** PostgreSQL
* **Ве-сервер:** Nginx
* **WSGI-сервер:** Gunicorn
* **Контейнеризация:** Docker, Docker Compose
* **CI/CD:** GitHub Actions (автоматические тесты, сборка и деплой на сервер)

---

## 🚀 Запуск проекта в Docker-контейнерах

### Предварительные требования
На вашем сервере должны быть установлены:
* Docker
* Docker Compose

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/ni-paa/foodgram.git
cd foodgram
```

### 2. Настройка переменных окружения
Создайте в корневой директории проекта файл `.env` и заполните его по примеру файла `.env.example`:

```bash
# Настройки Django
SECRET_KEY=your-secret-django-key
DEBUG=False
ALLOWED_HOSTS=your-server-ip-or-domain,localhost,127.0.0.1

# Настройки Базы Данных
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your-db-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432
```

### 3. Сборка и запуск контейнеров
Выполните команду из корня проекта:
```bash
docker-compose up -d
```

Сервис будет доступен по адресу `http://localhost/`.

### 4. Выполнение миграций и сбор статики
После успешного запуска контейнеров выполните:

```bash
# Применить миграции к базе данных
docker-compose exec backend python manage.py migrate

# Собрать статические файлы
docker-compose exec backend python manage.py collectstatic --no-input

# Создать суперпользователя (опционально, для доступа к админке)
docker-compose exec backend python manage.py createsuperuser
```

### 5. Загрузка начальных данных (ингредиенты и теги)
Для заполнения базы данных предустановленными ингредиентами и тегами выполните:
```bash
docker-compose exec backend python manage.py load_data
```

---

## 📁 Структура проекта

```
foodgram/
├── backend/                 # Django-приложение
│   ├── api/                # Django REST Framework (эндпоинты, сериализаторы)
│   ├── foodgram/           # Основные настройки проекта (settings.py, urls.py)
│   ├── recipes/            # Приложение "Рецепты" (модели, views)
│   ├── users/              # Приложение "Пользователи" (кастомная модель)
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # Статические файлы фронтенда (HTML, CSS, JS)
├── nginx/                  # Конфигурация Nginx
├── docker-compose.yml      # Конфигурация для запуска всех сервисов
├── Dockerfile              # Инструкция для сборки образа бэкенда
└── .github/workflows/      # Файлы для настройки CI/CD (GitHub Actions)
```

---

## 👨‍💻 Автор

**Антон Кравченко**

* GitHub: [MbIcJIu](https://github.com/ni-paa)