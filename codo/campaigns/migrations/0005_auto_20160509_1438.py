# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_auto_20160509_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2016, 6, 10, 14, 38, 46, 112900), blank=True),
        ),
        migrations.AlterField(
            model_name='organizer',
            name='dob',
            field=models.DateField(default=datetime.date(1975, 1, 1), blank=True),
        ),
    ]
