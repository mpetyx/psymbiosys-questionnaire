# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_auto_20170508_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='runinfo',
            name='campaign',
            field=models.ForeignKey(to='questionnaire.Campaign', null=True),
        ),
    ]
