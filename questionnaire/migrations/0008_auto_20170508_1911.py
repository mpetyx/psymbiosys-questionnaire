# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import multi_email_field.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questionnaire', '0007_auto_20170508_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Aidima Campaign', max_length=200)),
                ('emails', multi_email_field.fields.MultiEmailField()),
                ('manager', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='campaigns',
        ),
        migrations.AlterField(
            model_name='answer',
            name='campaign',
            field=models.ForeignKey(to='questionnaire.Campaign', null=True),
        ),
        migrations.AlterField(
            model_name='runinfohistory',
            name='campaign',
            field=models.ForeignKey(to='questionnaire.Campaign', null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='questionnaires',
            field=models.ManyToManyField(related_name='campaigns', to='questionnaire.Questionnaire', blank=True),
        ),
    ]
