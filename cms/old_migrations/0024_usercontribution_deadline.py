# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-09 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0023_auto_20170809_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercontribution',
            name='deadline',
            field=models.DateField(auto_now=True),
        ),
    ]