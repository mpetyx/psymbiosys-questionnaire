__author__ = 'mpetyx'

from questionnaire.models import *
from multi_email_field.fields import MultiEmailField
from django.contrib.auth.models import User

class Campaign(models.Model):

    manager = models.ForeignKey(User, blank=True)
    emails = MultiEmailField()
    questionnaires = models.ManyToManyField(Questionnaire, blank=True)