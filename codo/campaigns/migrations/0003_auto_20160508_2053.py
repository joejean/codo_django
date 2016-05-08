# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20160326_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2016, 6, 9, 20, 53, 19, 829149), blank=True),
        ),
        migrations.AlterField(
            model_name='organizer',
            name='dob',
            field=models.DateField(default=datetime.date(1960, 1, 1), blank=True),
        ),
    ]
