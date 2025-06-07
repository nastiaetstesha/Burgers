set -a
source .env
set +a
set -e

echo "Переход в папку проекта"
cd /opt/burgers

echo "Получение свежего кода из ветки server"
git pull origin server

echo "Получение свежих образов с Docker Hub (обновляем всегда)"
docker compose pull --quiet --ignore-pull-failures

# Альтернативно — если гарантировать обновление при запуске up:
# docker compose up --pull always -d

echo "Остановка и удаление старых контейнеров"
docker compose down --remove-orphans

echo "Применение миграций"
docker compose run --rm backend python manage.py migrate

echo "Сборка статики Django"
docker compose run --rm backend python manage.py collectstatic --noinput

echo "Запуск контейнеров в фоне"
docker compose up -d --pull always

echo "Очистка неиспользуемых Docker-образов"
docker image prune -f

echo "Готово! Контейнеры перезапущены."

echo "📤 Отправка информации о деплое в Rollbar"

REVISION=$(git rev-parse HEAD)
export GIT_COMMIT=$REVISION
echo $GIT_COMMIT

curl -X POST https://api.rollbar.com/api/1/deploy/ \
  -H "Content-Type: application/json" \
  -d "{
    \"access_token\": \"$ROLLBAR_TOKEN\",
    \"environment\": \"production\",
    \"revision\": \"$GIT_COMMIT\",
    \"local_username\": \"$(whoami)\",
    \"repository\": \"https://github.com/nastiaetstesha/Burgers.git\",
    \"branch\": \"server\"
  }"
