import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate.settings')
app = Celery('realestate', backend=settings.CELERY_RESULT_BACKEND, broker=settings.BROKER_URL)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # Executes every 10 min (10 sec for developing)
    'send-emails-every-10-minutes': {
        'task': 'notifications.tasks.send_email',
        'schedule': 10.0,   # crontab(minute='*/10'),
    },
}
