# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import multi_email_field.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questionnaire', '0009_runinfo_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='users',
            field=models.ManyToManyField(related_name='campaigns', null=True,
                                         verbose_name=b'Add participants emails',
                                         to='questionnaire.Subject', blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='emails',
            field=multi_email_field.fields.MultiEmailField(verbose_name=b'Add participants emails'),
        ),
    ]
