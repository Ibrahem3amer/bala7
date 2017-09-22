# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-10 16:59
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0014_auto_20170629_1548'),
        ('cms', '0003_topic_faculty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='N/A', max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')])),
                ('content', models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(50, 'Material Description should be more than 50 characters.')])),
                ('link', models.URLField(unique=True)),
                ('year', models.DateField()),
                ('term', models.PositiveIntegerField(choices=[(1, 'First term'), (2, 'Second term'), (3, 'Summer')])),
                ('content_type', models.PositiveIntegerField(choices=[(1, 'Lecture'), (2, 'Asset'), (3, 'Task')])),
                ('week_number', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='N/A', max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')])),
                ('bio', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(default='doctor.jpg', upload_to='')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('linkedn', models.URLField(blank=True, null=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professors', to='users.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='N/A', max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')])),
                ('content', models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(50, 'Material Description should be more than 50 characters.')])),
                ('link', models.URLField(unique=True)),
                ('year', models.DateField()),
                ('term', models.PositiveIntegerField(choices=[(1, 'First term'), (2, 'Second term'), (3, 'Summer')])),
                ('content_type', models.PositiveIntegerField(choices=[(1, 'Lecture'), (2, 'Asset'), (3, 'Task')])),
                ('week_number', models.PositiveIntegerField()),
                ('deadline', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopicTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topics', models.TextField()),
                ('places', models.TextField()),
                ('off_days', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
                ('json', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserContribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='N/A', max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')])),
                ('content', models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(50, 'Material Description should be more than 50 characters.')])),
                ('link', models.URLField(unique=True)),
                ('year', models.DateField()),
                ('term', models.PositiveIntegerField(choices=[(1, 'First term'), (2, 'Second term'), (3, 'Summer')])),
                ('content_type', models.PositiveIntegerField(choices=[(1, 'Lecture'), (2, 'Asset'), (3, 'Task')])),
                ('week_number', models.PositiveIntegerField()),
                ('status', models.PositiveIntegerField(choices=[(1, 'Pending'), (2, 'Rejected'), (3, 'Accepted')], default=1)),
                ('supervisior_id', models.PositiveIntegerField(blank=True)),
                ('deadline', models.DateField(blank=True, default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topics', models.TextField()),
                ('places', models.TextField()),
                ('off_days', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
                ('json', models.TextField()),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='table', to='users.UserProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='topic',
            name='weeks',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')]),
        ),
        migrations.AddField(
            model_name='usercontribution',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_materials', to='cms.Topic'),
        ),
        migrations.AddField(
            model_name='usercontribution',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_materials', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topictable',
            name='topic',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='table', to='cms.Topic'),
        ),
        migrations.AddField(
            model_name='task',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_tasks', to='cms.Topic'),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='material',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_materials', to='cms.Topic'),
        ),
        migrations.AddField(
            model_name='material',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_materials', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topic',
            name='professors',
            field=models.ManyToManyField(related_name='topics', to='cms.Professor'),
        ),
    ]
