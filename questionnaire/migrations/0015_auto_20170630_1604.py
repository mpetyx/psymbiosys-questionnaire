# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0014_auto_20170630_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='redirect_url',
            field=models.CharField(default=b'/complete.html', help_text=b'URL to redirect to when Questionnaire is complete. Macros: $SUBJECTID, $RUNID, $LANG', max_length=128),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='users',
            field=models.ManyToManyField(related_name='campaigns', verbose_name=b'Add participants emails', to='questionnaire.Subject', blank=True),
        ),
    ]
