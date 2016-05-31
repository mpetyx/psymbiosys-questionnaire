from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psy_questions.settings')

from django.conf import settings
from datetime import timedelta


app = Celery('proj')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



# app.conf.update(CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'email_campaigns.tasks.check_who_filled_the_questionaire',
#         'schedule': timedelta(seconds=4),
#         # 'args': (16, 16)
#     },
# }
# )

CELERY_TIMEZONE = 'UTC'

if not os.environ.get('LOGNAME')=='mpetyx':
    app.conf.update(BROKER_URL=os.getenv('CLOUDAMQP_URL', 'redis://localhost:6379'),
                    CELERY_RESULT_BACKEND=None)
    app.conf.update(BROKER_POOL_LIMIT=1)
    app.conf.update(CELERY_EVENT_QUEUE_EXPIRES = 120)
    app.conf.update(CELERY_EVENT_QUEUE_TTL= 60)
else:
    app.conf.update(BROKER_URL=os.getenv('REDISTOGO_URL', 'redis://localhost:6379'),
                CELERY_RESULT_BACKEND=os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))