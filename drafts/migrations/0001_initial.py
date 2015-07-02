# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('current_title', models.CharField(max_length=240)),
                ('current_version', models.IntegerField()),
                ('date_created', models.DateField(verbose_name='date_created', auto_now_add=True)),
            ],
        ),
    ]
