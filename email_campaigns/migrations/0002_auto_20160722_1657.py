# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0005_auto_20160722_1502'),
        ('email_campaigns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloneQuestionnaire',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('questionnaire.questionnaire',),
        ),
        migrations.AddField(
            model_name='campaign',
            name='name',
            field=models.CharField(default=b'Aidima Campaign', max_length=200),
        ),
    ]
