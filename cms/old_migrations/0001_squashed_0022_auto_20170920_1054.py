# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-20 11:11
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import re


class Migration(migrations.Migration):

    replaces = [('cms', '0001_initial'), ('cms', '0002_auto_20170602_1821'), ('cms', '0003_topic_faculty'), ('cms', '0004_auto_20170810_1659'), ('cms', '0005_auto_20170813_1641'), ('cms', '0006_exam'), ('cms', '0007_auto_20170814_1329'), ('cms', '0008_userpost'), ('cms', '0009_usercomment'), ('cms', '0010_auto_20170814_2224'), ('cms', '0011_usercomment_status'), ('cms', '0012_auto_20170904_1611'), ('cms', '0013_auto_20170904_1941'), ('cms', '0014_auto_20170904_1944'), ('cms', '0015_auto_20170904_1944'), ('cms', '0016_event'), ('cms', '0017_auto_20170907_1646'), ('cms', '0018_auto_20170908_1738'), ('cms', '0019_auto_20170908_1948'), ('cms', '0020_exam_exam_year'), ('cms', '0021_auto_20170920_0949'), ('cms', '0022_auto_20170920_1054')]

    initial = True

    dependencies = [
        ('users', '0011_auto_20170517_1952'),
        ('users', '0025_auto_20170919_2120'),
        ('users', '0014_auto_20170629_1548'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0013_auto_20170604_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')])),
                ('desc', models.CharField(max_length=400)),
                ('term', models.PositiveIntegerField(choices=[(1, 'First term'), (2, 'Second term'), (3, 'Summer')])),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='users.Department')),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='users.Faculty')),
                ('weeks', models.PositiveIntegerField(default=0)),
            ],
        ),
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
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_materials', to='cms.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_materials', to=settings.AUTH_USER_MODEL)),
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
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(50, 'Material Description should be more than 50 characters.')])),
                ('link', models.URLField(unique=True)),
                ('year', models.DateField(auto_now=True)),
                ('term', models.PositiveIntegerField(choices=[(1, 'First term'), (2, 'Second term'), (3, 'Summer')])),
                ('content_type', models.PositiveIntegerField(choices=[(1, 'Lecture'), (2, 'Asset'), (3, 'Task')])),
                ('week_number', models.PositiveIntegerField()),
                ('deadline', models.DateField(default=django.utils.timezone.now)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_tasks', to='cms.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_tasks', to=settings.AUTH_USER_MODEL)),
                ('professor', models.ManyToManyField(related_name='primary_tasks', to='cms.Professor')),
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
                ('topic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='table', to='cms.Topic')),
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
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(50, 'Material Description should be more than 50 characters.')])),
                ('link', models.URLField(unique=True)),
                ('year', models.DateField(auto_now=True)),
                ('term', models.PositiveIntegerField(choices=[(1, 'First term'), (2, 'Second term'), (3, 'Summer')])),
                ('content_type', models.PositiveIntegerField(choices=[(1, 'Lecture'), (2, 'Asset'), (3, 'Task')])),
                ('week_number', models.PositiveIntegerField()),
                ('status', models.PositiveIntegerField(choices=[(1, 'Pending'), (2, 'Rejected'), (3, 'Accepted')], default=1)),
                ('supervisior_id', models.PositiveIntegerField(blank=True, default=0)),
                ('deadline', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_materials', to='cms.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_materials', to=settings.AUTH_USER_MODEL)),
                ('professor', models.ManyToManyField(related_name='secondary_materials', to='cms.Professor')),
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
            name='professors',
            field=models.ManyToManyField(related_name='topics', to='cms.Professor'),
        ),
        migrations.AddField(
            model_name='material',
            name='professor',
            field=models.ManyToManyField(related_name='primary_materials', to='cms.Professor'),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='N/A', max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')])),
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(50, 'Material Description should be more than 50 characters.')])),
                ('link', models.URLField(unique=True)),
                ('year', models.DateField(auto_now=True)),
                ('term', models.PositiveIntegerField(choices=[(1, 'First term'), (2, 'Second term'), (3, 'Summer')])),
                ('content_type', models.PositiveIntegerField(choices=[(1, 'Lecture'), (2, 'Asset'), (3, 'Task')])),
                ('week_number', models.PositiveIntegerField()),
                ('professor', models.ManyToManyField(related_name='exams', to='cms.Professor')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='cms.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to=settings.AUTH_USER_MODEL)),
                ('exam_year', models.PositiveIntegerField(choices=[(1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=2017)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='material',
            name='content',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(50, 'Material Description should be more than 50 characters.')]),
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='N/A', max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')])),
                ('content', models.TextField()),
                ('status', models.PositiveIntegerField(choices=[(1, 'Pending'), (2, 'Rejected'), (3, 'Accepted')], default=1)),
                ('supervisior_id', models.PositiveIntegerField(blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='cms.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cms.UserPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('status', models.PositiveIntegerField(choices=[(0, 'Blocked'), (1, 'Accepted')], default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='userpost',
            name='supervisior_id',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='material',
            name='year',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='N/A', max_length=200, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')])),
                ('content', models.TextField(validators=[django.core.validators.MaxLengthValidator(200, 'Event description should not be more than 300 characters.')])),
                ('all_app', models.BooleanField(default=False)),
                ('deadline', models.DateField(default=django.utils.timezone.now)),
                ('dep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_events', to='users.Department')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faculty_events', to='users.Faculty')),
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='university_events', to='users.University')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='topic',
            name='department',
        ),
        migrations.AddField(
            model_name='topic',
            name='department',
            field=models.ManyToManyField(related_name='topics', to='users.Department'),
        ),
    ]
