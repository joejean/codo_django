# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import phonenumber_field.modelfields
import annoying.fields
import django_countries.fields
import django.utils.timezone
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=100)),
                ('blurb', models.CharField(max_length=300)),
                ('category', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('video_url', models.URLField(max_length=100)),
                ('picture', models.ImageField(upload_to='campaign_pics')),
                ('goal_amount', models.DecimalField(max_digits=15, decimal_places=2)),
                ('end_date', models.DateField(default=datetime.date.today)),
                ('rewards_enabled', models.BooleanField(default=False)),
                ('conditionals_enabled', models.BooleanField(default=False)),
                ('friends_participation_cond', models.BooleanField(default=False)),
                ('friends_participation_amount_cond', models.BooleanField(default=False)),
                ('community_participation_cond', models.BooleanField(default=False)),
                ('community_participation_amount_cond', models.BooleanField(default=False)),
                ('milestone_cond', models.BooleanField(default=False)),
                ('matching_donation_cond', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('unapproved', 'unapproved'), ('inreview', 'inreview'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='unapproved', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('short_bio', models.TextField()),
                ('profile_picture', models.ImageField(upload_to='profile_pics')),
                ('facebook_url', models.URLField(max_length=100)),
                ('twitter_url', models.URLField(max_length=100)),
                ('website_url', models.URLField(max_length=100)),
                ('dob', models.DateField(default=datetime.date.today)),
                ('user', annoying.fields.AutoOneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('pledge_amount', models.DecimalField(max_digits=15, decimal_places=2)),
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
