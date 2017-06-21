# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0011_auto_20170621_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='emails',
        )
    ]
