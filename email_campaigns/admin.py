__author__ = 'mpetyx'

from django.contrib import admin
from .models import Campaign
from signals import *


class CampaignAdmin(admin.ModelAdmin):
    pass

admin.site.register(Campaign, CampaignAdmin)
