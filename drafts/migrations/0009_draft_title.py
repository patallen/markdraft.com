# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0008_auto_20150703_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='title',
            field=models.CharField(max_length=140, default='Untitled'),
        ),
    ]
