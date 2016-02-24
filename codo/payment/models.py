from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

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
        defualt=US_Dollar)
    account_number = models.CharField(max_length=150)
    routing_number = models.CharField(max_length=100, default="000000SS")

    def __str__(self):
        return "<BankAccount: {}>".format(self.id)

