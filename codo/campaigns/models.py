import moneyed 
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import date
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from model_utils import Choices 
from model_utils.models import TimeStampedModel


class Organizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    country = CountryField(blank_label='(select country)')
    phone_number = PhoneNumberField()
    short_bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics')
    facebook_url = models.URLField(max_length=100)
    twitter_url = models.URLField(max_length=100)
    website_url = models.URLField(max_length=100)
    dob = models.DateField(default=date.today)
    stripe_account_id = models.CharField(max_length=100,default='0')
    
    def has_stripe_account(self):
        return self.stripe_account_id != "0"

    def __str__(self):
        return "<Organizer: {}>".format(self.user.first_name)


class Campaign(TimeStampedModel): 
    organizer = models.ForeignKey(Organizer)
    title = models.CharField(max_length=100)
    blurb = models.CharField(max_length=300)
    category = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(max_length=100)
    picture = models.ImageField(upload_to='campaign_pics')
    goal_amount = MoneyField(max_digits=12, decimal_places=2, default_currency="USD")
    end_date = models.DateField(default=date.today)
    rewards_enabled = models.BooleanField(default=False)
    conditionals_enabled = models.BooleanField(default=False)
    friends_participation_cond = models.BooleanField(default=False)
    friends_participation_amount_cond = models.BooleanField(default=False)
    community_participation_cond = models.BooleanField(default=False)
    community_participation_amount_cond = models.BooleanField(default=False)
    milestone_cond = models.BooleanField(default=False)
    matching_donation_cond = models.BooleanField(default=False)
    STATUS = Choices('unapproved','inreview', 'accepted','rejected')
    status = models.CharField(choices=STATUS, default=STATUS.unapproved, max_length=20)

    def __str__(self):
        return "<Campaign: {}>".format(self.title)

class Reward(models.Model):
    campaign = models.ForeignKey(Campaign)
    title = models.CharField(max_length=100)
    pledge_amount = MoneyField(max_digits=12, decimal_places=2, default_currency="USD")
    number_funders = models.IntegerField()
    description = models.TextField()
    def __str__(self):
        return "<Reward: {}>".format(self.title)

class BankAccount(models.Model):

    """
    :param: country: Two-letter ISO code representing the country the bank \
                     account is located in.
    :param : currency:Three-letter ISO currency code representing the currency\
                     paid out to the bank account.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    country = models.CharField(max_length=5)
    currency = models.CharField(max_length=10)
    account_number = models.CharField(max_length=150)
    routing_number = models.CharField(max_length=100, default="000000SS")

    def __str__(self):
        return "<BankAccount: {}>".format(self.id)

