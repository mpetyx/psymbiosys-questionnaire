# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_subject_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answered_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 22, 15, 2, 20, 580000), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subject',
            name='type',
            field=models.CharField(default=b'VISITOR', max_length=30, null=True, choices=[(b'VISITOR', b'Visitor'), (b'WORKER', b'Worker'), (b'MANAGER', b'Manager')]),
        ),
    ]
