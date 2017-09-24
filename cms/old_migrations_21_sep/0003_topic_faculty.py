# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 01:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20170604_0126'),
        ('cms', '0002_auto_20170602_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='users.Faculty'),
        ),
    ]