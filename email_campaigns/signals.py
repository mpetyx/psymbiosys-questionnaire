__author__ = 'mpetyx'

from tasks import *


def a_campaign_created(sender, instance, created, **kwargs):
    # if created:
    print 'a campaign created'
    a_campaign_created_celery.delay(instance)

post_save.connect(a_campaign_created, sender=Campaign)
