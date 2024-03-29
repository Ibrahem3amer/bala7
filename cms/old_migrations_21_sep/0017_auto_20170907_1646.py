# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-07 16:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='event',
            name='link',
        ),
        migrations.RemoveField(
            model_name='event',
            name='term',
        ),
        migrations.RemoveField(
            model_name='event',
            name='week_number',
        ),
        migrations.RemoveField(
            model_name='event',
            name='year',
        ),
        migrations.AlterField(
            model_name='event',
            name='content',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(30, 'Event description should not be more than 30 characters.')]),
        ),
    ]
