#!/bin/sh
# Migrate the database first
export DJANGO_SETTINGS_MODULE="config.settings.production" &
python3 manage.py collectstatic --no-input &
python3 manage.py migrate sites & 
python3 manage.py makemigrations localized &
python3 manage.py makemigrations users &
python3 manage.py makemigrations masters &
python3 manage.py makemigrations schedules &
python3 manage.py migrate &
python3 manage.py update_translation_fields users &
python3 manage.py update_translation_fields masters &
python3 manage.py update_translation_fields localized &
python3 manage.py update_translation_fields schedules &
python3 manage.py collectstatic --noinput
python3 manage.py shell -c "from gabis.apps.users.models import User; User.objects.create_superuser('admin', 'herbew@gmail.com', 'adminGu31n1')" &
python3 manage.py shell -c "from gabis.apps.users.models import User; user = User.objects.get(username='admin'); user.types='001'; user.save()" &

python3 manage.py loaddata 001001_user & 
python3 manage.py runserver 0.0.0.0:9999 &
celery -A gabis.apps.backoffice worker -l info --pool=gevent &
celery -A gabis.apps.backoffice beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 
    
