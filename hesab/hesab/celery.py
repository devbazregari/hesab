from celery import Celery
import os 


app = Celery('hesab')

os.environ.setdefault('DJANGO_SETTINGS_MODULE','hesab.settings')

app.config_from_object('django.conf:settings' , namespace='CELERY')