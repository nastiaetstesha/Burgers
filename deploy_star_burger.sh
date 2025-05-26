set -a
source .env
set +a
set -e

echo " Переход в папку проекта"
cd /opt/burgers

echo "Получение свежего кода"
git pull

echo "Активация виртуального окружения"
source .venv/bin/activate

echo "Установка зависимостей"
pip install -r requirements.txt

echo "Установка Node.js-зависимостей"
npm ci

echo "Сборка фронтенда"
npm run build

echo "Сборка статики Django"
python manage.py collectstatic --noinput

echo "Применение миграций"
python manage.py migrate

echo "Перезапуск Gunicorn (star-burger)"
sudo systemctl restart star-burger.service

echo " Готово! Код обновлён и сервер перезапущен."
echo "📤 Отправка информации о деплое в Rollbar"

REVISION=$(git rev-parse HEAD)
export GIT_COMMIT=$(git rev-parse HEAD)

curl -X POST https://api.rollbar.com/api/1/deploy/ \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "'"$ROLLBAR_TOKEN"'",
    "environment": "production",
    "revision": "'"$REVISION"'",
    "local_username": "'"$(whoami)"'"
  }'
