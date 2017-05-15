__author__ = 'mpetyx'

from tasks import *
from django.db.models.signals import post_save, m2m_changed


# def a_campaign_created(sender, instance, **kwargs):
#     action = kwargs.get('action', None)
#     if not action or action == 'post_add':
#         a_campaign_modified(instance)
#
# post_save.connect(a_campaign_created, sender=Campaign)
# m2m_changed.connect(a_campaign_created, sender=Campaign.questionnaires.through)
