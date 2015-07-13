# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0009_draft_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='starred',
            field=models.BooleanField(default=True),
        ),
    ]
