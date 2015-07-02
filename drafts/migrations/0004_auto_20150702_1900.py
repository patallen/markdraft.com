# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0003_auto_20150702_1810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='current_version',
            new_name='latest_version',
        ),
        migrations.RemoveField(
            model_name='document',
            name='current_title',
        ),
    ]
