# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-14 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20170514_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='count_of_posts',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='count_of_replies',
            field=models.IntegerField(default=0),
        ),
    ]