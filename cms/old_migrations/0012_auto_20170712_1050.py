# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-12 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20170710_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='picture',
            field=models.ImageField(default='doctor.jpg', upload_to=''),
        ),
    ]
