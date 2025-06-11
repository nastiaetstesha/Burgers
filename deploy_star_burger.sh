set -a
source .env
set +a
set -e

echo " Переход в папку проекта"
cd /opt/burgers

echo "Получение свежего кода"
git pull origin server

echo "Получение свежих образов с Docker Hub"
docker compose pull --quiet

echo "Остановка старых контейнеров и удаление мусорных"
docker compose down --remove-orphans

echo "Очистка неиспользуемых образов"
docker image prune -f

echo "Применение миграций"
docker compose run --rm backend python manage.py migrate

echo "Сборка статики Django"
docker compose run --rm backend python manage.py collectstatic --noinput

echo "Запуск контейнеров в фоне"
docker compose up -d --pull always

echo "Готово! Контейнеры перезапущены."

echo "📤 Отправка информации о деплое в Rollbar"

REVISION=$(git rev-parse HEAD)
export GIT_COMMIT=$(git rev-parse HEAD)
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

