# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengelink',
            name='challengee',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='challengelink',
            name='challenger',
            field=models.CharField(max_length=45),
        ),
    ]
