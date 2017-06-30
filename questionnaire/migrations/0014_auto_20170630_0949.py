# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0013_auto_20170622_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='redirect_url',
        ),
        migrations.AddField(
            model_name='campaign',
            name='redirect_url',
            field=models.CharField(default=b'/static/complete.html', help_text=b'URL to redirect to when Questionnaire is complete. Macros: $SUBJECTID, $RUNID, $LANG', max_length=128),
        )
    ]
