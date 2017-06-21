# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_existing_emails(apps, schema_editor):
    Campaign = apps.get_model("questionnaire", "Campaign")
    Subject = apps.get_model("questionnaire", "Subject")

    for campaign in Campaign.objects.all():
        users = Subject.objects.filter(email__in=campaign.emails)
        for user in users:
            campaign.users.add(user)


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0010_auto_20170621_2048'),
    ]

    operations = [
        migrations.RunPython(migrate_existing_emails),
    ]
