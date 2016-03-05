# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_auto_20160219_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='goal_amount',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='reward',
            name='pledge_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
