# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_campaigns', '0002_auto_20160722_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='questionnaires',
            field=models.ManyToManyField(related_name='campaigns', to='questionnaire.Questionnaire', blank=True),
        ),
    ]
