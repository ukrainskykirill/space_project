import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'space.settings')
app = Celery('space')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'get_nasa_photo': {
        'task': 'get_photo',
        'schedule': crontab(minute='1', hour='0'),
        'args': (7,),
    },
    'get_asteroids': {
        'task': 'get_asteroids',
        'schedule': crontab(minute='1', hour='0'),
        'args': (7,),
    },
}


