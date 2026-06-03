# Frame Pit

FramePit - это веб-приложение для совместного просмотра YouTube видео в реальном времени. Пользователи могут создавать комнаты, приглашать друзей и смотреть видео с синхронизацией воспроизведения и чатом.

---

## Требования
* Git
* Docker
* Docker Compose

---

## Шаги запуска

### 1. Клонирование репозитория
```bash
git clone https://github.com/dobrso/FramePit.git
cd framepit
```
### 2. Переменные окружения
Создайте файл .env рядом с settings.py и установите переменные окружения
```
# Django
SECRET_KEY

# PostgreSQL
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

# Email
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
EMAIL_HOST
EMAIL_PORT
EMAIL_USE_SSL
EMAIL_USE_TLS

# Redis
REDIS_LOCATION (Можно использовать локальный Redis)
REDIS_PASSWORD
REDIS_HOST
REDIS_PORT

# Providers
GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET
YANDEX_CLIENT_ID
YANDEX_CLIENT_SECRET
```

### 3. Сборка и запуск проекта
```bash
docker-compose up --build
```