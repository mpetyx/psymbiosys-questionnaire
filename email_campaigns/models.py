__author__ = 'mpetyx'

from questionnaire.models import *
from multi_email_field.fields import MultiEmailField
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Campaign(models.Model):

    manager = models.ForeignKey(User, blank=True)
    emails = MultiEmailField()
    questionnaires = models.ManyToManyField(Questionnaire, blank=True)