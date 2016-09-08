# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0005_auto_20160722_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='type',
            field=models.CharField(default=b'WORKERS_SENTIMENT', max_length=256, choices=[(b'WORKERS_SENTIMENT', b'Workers Sentiment Questionnaire'), (b'BRAND_VALUE', b'Brand Value Questionnaire')]),
        ),
    ]
