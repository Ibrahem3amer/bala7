# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-14 11:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20170513_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fac_users', to='users.Faculty'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uni_users', to='users.University'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depart_users', to='users.Department'),
        ),
    ]
