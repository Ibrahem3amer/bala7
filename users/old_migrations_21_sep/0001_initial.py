# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-28 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uni_type', models.CharField(max_length=200)),
                ('bio', models.CharField(max_length=200)),
            ],
        ),
    ]
