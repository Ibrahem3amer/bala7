# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-01 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170430_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_type', models.CharField(default='normal', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='university',
            name='headmaster',
            field=models.CharField(default='Professors name', max_length=200),
        ),
        migrations.AddField(
            model_name='university',
            name='location',
            field=models.CharField(default='no data initialized', max_length=200),
        ),
        migrations.AddField(
            model_name='university',
            name='rank',
            field=models.IntegerField(default=-1),
        ),
    ]