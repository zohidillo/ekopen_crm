# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset
export DJANGO_SETTINGS_MODULE=config.settings.development

echo "Running migrations..."
#python manage.py makemigrations main --noinput
#python manage.py migrate main --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Running tests..."
python manage.py test
echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000
