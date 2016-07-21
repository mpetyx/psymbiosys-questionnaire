# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_auto_20160531_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='type',
            field=models.CharField(default=b'VISITOR', max_length=30, choices=[(b'VISITOR', b'Visitor'), (b'WORKER', b'Worker'), (b'MANAGER', b'Manager')]),
        ),
    ]
