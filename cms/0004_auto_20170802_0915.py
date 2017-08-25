# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-02 09:15
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20170802_0915'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='TopicTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.CharField(max_length=200)),
                ('topics', models.CharField(max_length=200)),
                ('places', models.CharField(max_length=200)),
                ('off_days', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
                ('json', models.CharField(max_length=200)),
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
        migrations.CreateModel(
            name='Task',
            fields=[
                ('material_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cms.Material')),
                ('deadline', models.DateField()),
            ],
            bases=('cms.material',),
        ),
        migrations.AddField(
            model_name='topictable',
            name='topic',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='table', to='cms.Topic'),
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