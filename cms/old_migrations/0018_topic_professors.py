# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-01 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0017_auto_20170730_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='professors',
            field=models.ManyToManyField(related_name='topics', to='cms.Professor'),
        ),
    ]