# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_campaigns', '0004_remove_campaign_questionnaires'),
        ('questionnaire', '0006_questionnaire_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='campaign',
            field=models.ForeignKey(to='email_campaigns.Campaign', null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='campaigns',
            field=models.ManyToManyField(related_name='questionnaires', to='email_campaigns.Campaign', blank=True),
        ),
        migrations.AddField(
            model_name='runinfohistory',
            name='campaign',
            field=models.ForeignKey(to='email_campaigns.Campaign', null=True),
        ),
    ]
