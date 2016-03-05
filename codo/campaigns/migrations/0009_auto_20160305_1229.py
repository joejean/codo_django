# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_auto_20160304_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizer',
            name='stripe_account_id',
        ),
        migrations.AlterField(
            model_name='campaign',
            name='goal_amount',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='reward',
            name='pledge_amount',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
