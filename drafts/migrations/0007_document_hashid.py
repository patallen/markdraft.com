# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0006_remove_document_latest_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='hashid',
            field=models.CharField(db_index=True, default='null', max_length=10),
            preserve_default=False,
        ),
    ]
