# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-04 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_usercomment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='year',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='year',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='year',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='usercontribution',
            name='year',
            field=models.DateField(auto_now=True),
        ),
    ]