# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-29 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_note_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
