# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0006_auto_20160227_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='user',
        ),
        migrations.AddField(
            model_name='organizer',
            name='stripe_account_id',
            field=models.CharField(max_length=100, default='0'),
        ),
        migrations.DeleteModel(
            name='BankAccount',
        ),
    ]
