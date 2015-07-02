# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0004_auto_20150702_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draft',
            name='document',
            field=models.ForeignKey(to='drafts.Document', related_name='drafts'),
        ),
    ]
