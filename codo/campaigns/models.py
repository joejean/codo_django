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
from payments.models import Merchant,Account

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
    
    def get_wepay_access_token(self):
        merchant = Merchant.objects.filter(user=self.user)
        if merchant:
            return merchant[0].access_token
        return None

    def get_wepay_user_id(self):
        merchant = Merchant.objects.filter(user=self.user)
        if merchant:
            return merchant[0].wepay_user_id
        return None

    def get_wepay_account_id(self):
        account = Account.objects.filter(user=self.user)
        if account:
            return account[0].account_id
        return None

    def get_wepay_account_uri(self):
        account = Account.objects.filter(user=self.user)
        if account:
            return account[0].account_uri
        return None


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
    goal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    #MoneyField(max_digits=12, decimal_places=2, default_currency="USD")
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
    pledge_amount = models.DecimalField(max_digits=15, decimal_places=2)
    #MoneyField(max_digits=12, decimal_places=2, default_currency="USD")
    number_funders = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return "<Reward: {}>".format(self.title)

