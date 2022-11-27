import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpyrus.settings')

app = Celery('djpyrus')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print-huy-every-minute': {
        'task': 'app_pyrus.tasks.load',
        'schedule': crontab(minute='0', hour='4'),
    },
}
