__author__ = 'mpetyx'

# pip install hirefire

from celery import Celery

from hirefire.procs.celery import CeleryProc

celery = Celery('myproject', broker='amqp://guest@localhost//')


class WorkerProc(CeleryProc):
    # the name field should be identical with the worker name on your Procfile!! It is nowhere explicitly written, but otherwise it won't work!
    name = 'worker'
    queues = ['celery']
    app = celery
