# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drafts', '0002_draft_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_title', models.CharField(max_length=240)),
                ('current_version', models.IntegerField()),
                ('date_created', models.DateField(verbose_name='date_created', auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='draft',
            old_name='current_version',
            new_name='version',
        ),
        migrations.RemoveField(
            model_name='draft',
            name='current_title',
        ),
        migrations.RemoveField(
            model_name='draft',
            name='user',
        ),
        migrations.AddField(
            model_name='draft',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='draft',
            name='document',
            field=models.ForeignKey(default=1, to='drafts.Document'),
            preserve_default=False,
        ),
    ]
