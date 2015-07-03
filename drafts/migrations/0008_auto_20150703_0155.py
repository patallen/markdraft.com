# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0007_document_hashid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='date_created',
        ),
        migrations.AlterField(
            model_name='draft',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
