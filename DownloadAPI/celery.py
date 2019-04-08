import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DownloadAPI.settings')

app = Celery('DownloadAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()