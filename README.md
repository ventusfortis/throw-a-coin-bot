# Throw a Coin Bot

Telegram-бот, который подбрасывает монетку. Работает **в любых чатах без добавления** через inline-режим.

## Как пользоваться

В любом чате (личка, группа, канал с комментариями):

1. Наберите `@имя_вашего_бота`
2. Выберите «Подбросить монетку»
3. Результат отправится в чат

В личных сообщениях с ботом: `/flip`

## Настройка

### 1. Создать бота в [@BotFather](https://t.me/BotFather)

- `/newbot` — получить токен
- `/setinline` — включить inline-режим (обязательно для работы в чатах без добавления)
- При запросе placeholder можно указать, например: `подбросить монетку`

### 2. Установка и запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Вставьте токен в .env
python bot.py
```

## Деплой на VPS (Docker)

На сервере нужны [Docker](https://docs.docker.com/engine/install/) и Docker Compose (плагин `docker compose`).

```bash
# Клонировать репозиторий на VPS
git clone <url-репозитория> throw-a-coin-bot
cd throw-a-coin-bot

# Токен бота (не коммитить в git)
cp .env.example .env
nano .env   # BOT_TOKEN=...

# Сборка и запуск в фоне
docker compose up -d --build

# Логи
docker compose logs -f bot
```

Обновление после изменений в коде:

```bash
git pull
docker compose up -d --build
```

Остановка:

```bash
docker compose down
```

Контейнер перезапускается автоматически (`restart: unless-stopped`). Webhook и открытые порты не нужны — бот сам опрашивает Telegram (long polling).

## Почему inline

Обычные команды (`/flip`) в группах работают только если бот добавлен в чат. Inline-запросы (`@bot` в поле ввода) доступны везде, где Telegram разрешает упоминать ботов — бота в группу добавлять не нужно.
