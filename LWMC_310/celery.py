import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'LWMC_310.settings')
celery=Celery('LWMC_310')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()