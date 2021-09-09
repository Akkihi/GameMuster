import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamewebsite.settings')

app = Celery('gamewebsite')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-db': {
        'task': 'main.tasks.update_db',
        'schedule': 1500.0
    }
}