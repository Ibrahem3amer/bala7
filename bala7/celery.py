import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bala7.settings.base')

app = Celery('bala7')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()