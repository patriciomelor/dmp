from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmp.settings')

app = Celery('dmp')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.conf.timezone = 'America/Santiago'

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)


