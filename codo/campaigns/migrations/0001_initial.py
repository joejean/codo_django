# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import phonenumber_field.modelfields
import django_countries.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=5)),
                ('currency', models.CharField(max_length=10)),
                ('account_number', models.CharField(max_length=150)),
                ('routing_number', models.CharField(default='000000SS', max_length=100)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('blurb', models.CharField(max_length=300)),
                ('category', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('video_url', models.URLField(max_length=100)),
                ('picture', models.ImageField(upload_to='/campaign_pics')),
                ('goal_amount', models.DecimalField(max_digits=19, decimal_places=10)),
                ('end_date', models.DateField(default=datetime.date.today)),
                ('rewards_enabled', models.BooleanField(default=False)),
                ('conditionals_enabled', models.BooleanField(default=False)),
                ('friends_participation_cond', models.BooleanField(default=False)),
                ('friends_participation_amount_cond', models.BooleanField(default=False)),
                ('community_participation_cond', models.BooleanField(default=False)),
                ('community_participation_amount_cond', models.BooleanField(default=False)),
                ('milestone_cond', models.BooleanField(default=False)),
                ('matching_donation_cond', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('short_bio', models.TextField()),
                ('profile_picture', models.ImageField(upload_to='/profile_pics')),
                ('facebook_url', models.URLField(max_length=100)),
                ('twitter_url', models.URLField(max_length=100)),
                ('website_url', models.URLField(max_length=100)),
                ('dob', models.DateField(default=datetime.date.today)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length='100')),
                ('pledge_amount', models.DecimalField(max_digits=19, decimal_places=10)),
                ('number_funders', models.IntegerField()),
                ('description', models.TextField()),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='organizer',
            field=models.ForeignKey(to='campaigns.Organizer'),
        ),
    ]
