from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from django_countries.fields import CountryField



class Merchant(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    access_token = models.CharField(null=True, max_length=255)
    wepay_user_id = models.CharField(null=True, max_length=255)

    def __str__(self):
        return "<Merchant: wepay user id {}. Access Token {}. User {}>".format(\
            self.wepay_user_id, self.access_token, self.user.first_name)

class Account(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    account_id = models.CharField(max_length=255)
    account_uri = models.CharField(max_length=255)

    def __str__(self):
        return "<Account: account  id {}. Account URI {}>".format(\
            self.account_id, self.account_uri)

class DirectDonation(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    campaign = models.ForeignKey('campaigns.Campaign')
    amount = models.DecimalField(max_digits=15, decimal_places=2)

class ConditionalDonation(models.Model):
    pass



class BankAccount(models.Model):
    """
    :param: country: Two-letter ISO code representing the country the bank \
                     account is located in.
    :param : currency:Three-letter ISO currency code representing the currency\
                     paid out to the bank account.
    """
    Can_Dollar = "CAD"
    US_Dollar = "USD"
    CURRENCY_CHOICES = (
        (US_Dollar, "US Dollar"),
        (Can_Dollar, "Canadian Dollar"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    country = CountryField(blank_label='(select country)')
    currency = models.CharField(max_length=3, choices= CURRENCY_CHOICES,\
        default=US_Dollar)
    account_number = models.CharField(max_length=150)
    routing_number = models.CharField(max_length=100, default="000000SS")

    def __str__(self):
        return "<BankAccount: {}>".format(self.id)




