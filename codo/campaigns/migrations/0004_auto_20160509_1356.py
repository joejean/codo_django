# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_auto_20160508_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2016, 6, 10, 13, 56, 35, 253601), blank=True),
        ),
    ]
