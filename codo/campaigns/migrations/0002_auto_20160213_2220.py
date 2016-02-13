# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='status',
            field=models.CharField(default='unapproved', max_length=20, choices=[('unapproved', 'unapproved'), ('inreview', 'inreview'), ('accepted', 'accepted'), ('rejected', 'rejected')]),
        ),
        migrations.AlterField(
            model_name='reward',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
