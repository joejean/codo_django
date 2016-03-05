# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0007_auto_20160304_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='goal_amount_currency',
        ),
        migrations.RemoveField(
            model_name='reward',
            name='pledge_amount_currency',
        ),
        migrations.AlterField(
            model_name='campaign',
            name='goal_amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='reward',
            name='pledge_amount',
            field=models.IntegerField(),
        ),
    ]
