# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20160326_2304'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=100)),
                ('port', models.CharField(max_length=40)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('challenges', models.IntegerField()),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pledge', models.TextField()),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('challengee', models.ForeignKey(related_name='challengee_user', to=settings.AUTH_USER_MODEL)),
                ('challenger', models.ForeignKey(related_name='challenger_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pledge', models.TextField()),
                ('resolved', models.DecimalField(default=0.0, decimal_places=2, max_digits=15)),
                ('changed_on', models.DateField(default=datetime.date.today)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('category', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submitted_on', models.DateTimeField(default=datetime.datetime.now)),
                ('pledge', models.TextField()),
                ('total_before', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_after', models.DecimalField(decimal_places=2, max_digits=15)),
                ('impact', models.DecimalField(decimal_places=2, max_digits=15)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=40)),
                ('member', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=100)),
                ('port', models.CharField(max_length=40)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('hasDon', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('group_name', 'member')]),
        ),
        migrations.AlterUniqueTogether(
            name='condition',
            unique_together=set([('user', 'campaign')]),
        ),
        migrations.AlterUniqueTogether(
            name='challengelink',
            unique_together=set([('campaign', 'challenger', 'challengee')]),
        ),
    ]
