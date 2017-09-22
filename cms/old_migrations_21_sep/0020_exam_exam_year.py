# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-20 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0019_auto_20170908_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='exam_year',
            field=models.PositiveIntegerField(choices=[(1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=2000),
            preserve_default=False,
        ),
    ]
