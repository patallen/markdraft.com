# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0005_auto_20150702_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='latest_version',
        ),
    ]
