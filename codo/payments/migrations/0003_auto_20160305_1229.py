# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaigns', '0009_auto_20160305_1229'),
        ('payments', '0002_auto_20160305_0139'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditionalDonation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DirectDonation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='account',
            name='created',
            field=model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='account',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='merchant',
            name='created',
            field=model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='merchant',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now),
        ),
    ]
