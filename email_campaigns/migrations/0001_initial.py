# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import multi_email_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_auto_20160531_1535'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('emails', multi_email_field.fields.MultiEmailField()),
                ('manager', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
                ('questionnaires', models.ManyToManyField(to='questionnaire.Questionnaire', blank=True)),
            ],
        ),
    ]
