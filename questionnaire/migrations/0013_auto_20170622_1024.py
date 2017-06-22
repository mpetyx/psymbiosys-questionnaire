# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0012_auto_20170621_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='manager',
        ),
        migrations.AddField(
            model_name='campaign',
            name='director',
            field=models.ForeignKey(default=15, to='questionnaire.Subject'),
            preserve_default=False,
        ),

    ]
