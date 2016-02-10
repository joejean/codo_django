from django.db import models
from django.utils import timezone
from django.conf import settings


class Organizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # country =
    # phone_number =
    # short_bio = 
    # profile_picture =
    # facebook_url = 
    # twitter_url =
    # website_url = 
    # dob = models.DateField()
    # stripe_account_id = models.CharField(max_length=150)
    
    # def __str__(self):
    #     return "<Organizer: {}>".format(self.user.first_name)


class Campaign(models.Model):
    organizer = models.ForeignKey(Organizer)
    title = models.CharField(max_length=100)
    blurb = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='/campaign_pics')
    goal_amount = models.DecimalField(max_digits=19, decimal_places=10)
    end_date = models.DateField(default=timezone.now)
    rewards_enabled = models.BooleanField(default=False)
    conditionals_enabled = models.BooleanField(default=False)
    friends_participation_cond = models.BooleanField(default=False)
    friends_participation_amount_cond = models.BooleanField(default=False)
    community_participation_cond = models.BooleanField(default=False)
    community_participation_amount_cond = models.BooleanField(default=False)
    milestone_cond = models.BooleanField(default=False)
    matching_donation_cond = models.BooleanField(default=False)

    def __str__(self):
        return "<Campaign: {}>".format(self.title)

class Reward(models.Model):
    campaign = models.ForeignKey(Campaign)
    title = models.CharField(max_length="100")
    pledge_amount = models.DecimalField(max_digits=19, decimal_places=10)
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

