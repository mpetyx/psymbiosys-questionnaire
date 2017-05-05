__author__ = 'mpetyx'

from tasks import *


def a_campaign_created(sender, instance, created, **kwargs):
    a_campaign_modified.delay(instance)

post_save.connect(a_campaign_created, sender=Campaign)
