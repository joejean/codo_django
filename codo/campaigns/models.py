import moneyed 
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from model_utils import Choices 
from model_utils.models import TimeStampedModel
from payments.models import Merchant,Account
from django.core.urlresolvers import reverse
from annoying.fields import AutoOneToOneField


class Organizer(models.Model):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL)
    country = CountryField(blank_label='(select country)')
    phone_number = PhoneNumberField(blank=True)
    short_bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics')
    facebook_url = models.URLField(max_length=100)
    twitter_url = models.URLField(max_length=100)
    website_url = models.URLField(max_length=100)
    dob = models.DateField(default=datetime.date(1975,1,1),blank=True)

    def profile_picture_tag(self):
        '''This is used to help render the image in the admin field'''
        return u'<img src="%s" width="400" height="300" />' % self.profile_picture.url
    profile_picture_tag.short_description = 'Image'
    profile_picture_tag.allow_tags = True

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})
    
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
        return self.user.get_full_name()


class Campaign(TimeStampedModel): 
    ''' Campaign Model. The TimeStampedModel provides self-updating created and 
        modified fields on any model that inherits from it. See
        http://django-model-utils.readthedocs.io/en/latest/models.html
    '''
    organizer = models.ForeignKey(Organizer)
    title = models.CharField(max_length=100)
    blurb = models.CharField(max_length=300)
    category = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(max_length=100)
    picture = models.ImageField(upload_to='campaign_pics')
    goal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    #MoneyField(max_digits=12, decimal_places=2, default_currency="USD")
    end_date = models.DateField(default=datetime.datetime.now()+datetime.timedelta(days=32)
    ,blank=True)
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

    def image_tag(self):
        '''This is used to help render the image in the admin field'''
        return u'<img src="%s" width="400" height="300"/>' % self.picture.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def get_days_left(self):
        num_days = (self.end_date - date.today()).days
        return num_days if num_days>=0 else 0

    def get_absolute_url(self):
        return reverse('single_campaign', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Reward(models.Model):
    campaign = models.ForeignKey(Campaign)
    title = models.CharField(max_length=100)
    pledge_amount = models.DecimalField(max_digits=15, decimal_places=2)
    #MoneyField(max_digits=12, decimal_places=2, default_currency="USD")
    number_funders = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return self.title

