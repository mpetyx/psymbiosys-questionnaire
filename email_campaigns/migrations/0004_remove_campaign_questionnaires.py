# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_campaigns', '0003_auto_20160907_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='questionnaires',
        ),
    ]
