from django.db import models
from django.contrib.auth.models import User


class Organizer(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateField()
    stripe_account_id = models.CharField(max_length=150)
    
    def __str__(self):
        return "<Organizer: {}>".format(self.user.first_name)


class Campaign(models.Model):
    organizer = models.ForeignKey(Organizer)
    name = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=100)

    def __str__(self):
        return "<Campaign: {}>".format(self.name)


class BankAccount(models.Model):

    """
    :param: country: Two-letter ISO code representing the country the bank \
                     account is located in.
    :param : currency:Three-letter ISO currency code representing the currency\
                     paid out to the bank account.
    """
    user = models.OneToOneField(User)
    country = models.CharField(max_length=5)
    currency = models.CharField(max_length=10)
    account_number = models.CharField(max_length=150)
    routing_number = models.CharField(max_length=100, default="000000SS")

    def __str__(self):
        return "<BankAccount: {}>".format(self.id)

