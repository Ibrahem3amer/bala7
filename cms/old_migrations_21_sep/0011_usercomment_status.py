# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-15 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_auto_20170814_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Blocked'), (1, 'Accepted')], default=1),
        ),
    ]
