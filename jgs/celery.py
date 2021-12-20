from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from django.conf import settings

from celery.schedules import crontab

from django.utils import timezone

from datetime import timezone


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jgs.settings')

app = Celery('jgs')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

app.config_from_object('django.conf:settings', namespace='CELERY')


# Celery beat settings 

app.conf.beat_schedule = {
    'send-expiry-email-everyday': {
        'task': 'control.tasks.send_expiry_mail',
        'schedule': crontab(hour=7, minute=0)
    } 
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')