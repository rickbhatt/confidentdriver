release: python manage.py migrate
web: gunicorn jgs.wsgi --log-file -
celery: celery -A jgs.celery worker --pool=solo -l info