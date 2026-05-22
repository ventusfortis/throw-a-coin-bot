#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
IMAGE=throw-a-coin-bot
CONTAINER=throw-a-coin-bot

if [[ ! -f .env ]]; then
  echo "Создайте .env с BOT_TOKEN (см. .env.example)" >&2
  exit 1
fi

docker build -t "$IMAGE" .
docker stop "$CONTAINER" 2>/dev/null || true
docker rm "$CONTAINER" 2>/dev/null || true
docker run -d \
  --name "$CONTAINER" \
  --restart unless-stopped \
  --env-file .env \
  "$IMAGE"

echo "Запущен: $CONTAINER"
echo "Логи: docker logs -f $CONTAINER"
