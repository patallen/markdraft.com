# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0010_document_starred'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='starred',
            field=models.BooleanField(default=False),
        ),
    ]
