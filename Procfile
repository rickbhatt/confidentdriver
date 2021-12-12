web: gunicorn jgs.wsgi --log-file -
worker: celery worker --app=tasks.app