from django.db import models

# Create your models here.

class ChallengeLink(models.Model):
    challenger
    challengee
    pledge

class Conditions(models.Model):
    user
    pledge
    resolved


