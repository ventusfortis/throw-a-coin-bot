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

Нужен только Docker. Compose не обязателен.

```bash
git clone https://github.com/ventusfortis/throw-a-coin-bot.git
cd throw-a-coin-bot

cp .env.example .env
nano .env   # BOT_TOKEN=...

chmod +x deploy.sh
./deploy.sh
```

`deploy.sh` собирает образ и запускает контейнер через `docker run` (удобно на Ubuntu 20.04, где нет `docker compose`).

Логи без перезапуска:

```bash
docker logs -f throw-a-coin-bot
```

Обновление:

```bash
git pull
./deploy.sh
```

Остановка:

```bash
docker stop throw-a-coin-bot
```

### Вариант с Compose (если установлен)

В `docker-compose.yml` указано `version: "3.8"` — нужно для старого `docker-compose` v1.

```bash
docker-compose up -d --build    # Ubuntu 20.04, пакет docker-compose
# или
docker compose up -d --build    # если есть плагин compose v2
```

На Ubuntu 20.04 пакет `docker-compose-plugin` в стандартных репозиториях часто отсутствует. Плагин можно поставить вручную:

```bash
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m)" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
docker compose version
```

Контейнер перезапускается автоматически (`restart: unless-stopped`). Порты наружу не нужны — long polling.

## Inline не работает — чеклист

1. **Тот же бот, что на VPS.** Напишите боту `/start` — в ответе будет `@username`. Именно его набирайте в чате, не другой бот из BotFather.

2. **BotFather:** `/setinline` → выберите бота → placeholder (например `монетка`). Без этого inline не включится.

3. **Как вызывать:** в поле **сообщения** чата (не поиск) наберите `@username_бота`, подождите список, нажмите «Подбросить монетку». Команда `/flip` в группе без добавления бота не сработает — только inline.

4. **Логи на VPS:**
   ```bash
   docker logs throw-a-coin-bot 2>&1 | tail -30
   ```
   При наборе `@бот` должна появиться строка `inline_query`. Если её нет — запросы не доходят (часто другой токен, webhook или inline выключен).

5. **Webhook:** если бот когда-то работал на webhook, сбросьте:
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook?drop_pending_updates=true"
   ```
   Перезапустите контейнер.

6. **Один процесс:** `docker ps` — не должно быть двух контейнеров с одним ботом.

7. **Первый раз:** откройте личку с ботом и нажмите Start — в некоторых клиентах так появляется inline в других чатах.

## Почему inline

Обычные команды (`/flip`) в группах работают только если бот добавлен в чат. Inline-запросы (`@bot` в поле ввода) доступны везде, где Telegram разрешает упоминать ботов — бота в группу добавлять не нужно.
