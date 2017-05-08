# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_auto_20170508_1911'),
        ('email_campaigns', '0004_remove_campaign_questionnaires'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='manager',
        ),
        migrations.DeleteModel(
            name='Campaign',
        ),
    ]
