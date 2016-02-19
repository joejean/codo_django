# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20160213_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='picture',
            field=models.ImageField(upload_to='campaign_pics'),
        ),
        migrations.AlterField(
            model_name='organizer',
            name='profile_picture',
            field=models.ImageField(upload_to='profile_pics'),
        ),
    ]
