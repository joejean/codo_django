from datetime import date, datetime
from django.db import models
from django.conf import settings
from campaigns.models import Campaign

#TODO: This PROBABLY needs Campaign as a FK here as well
class Amount_Log(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	ip = models.CharField(max_length=100)
	port = models.CharField(max_length=40)	
	time = models.DateTimeField(default= datetime.now)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	challenges = models.IntegerField()
	
	def __str__(self):
		return "{}, {}, {}, {}, {}, {}".format(self.ip,self.port,self.time,self.username,self.amount,self.challenges)

#TODO: This needs Campaign as a FK here as well		
class Log(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, primary_key=True)
	submitted_on = models.DateTimeField(default= datetime.now)
	pledge = models.TextField()
	total_before = models.DecimalField(max_digits=15, decimal_places=2)
	total_after = models.DecimalField(max_digits=15, decimal_places=2)
	impact = models.DecimalField(max_digits=15, decimal_places=2)

	def __str__(self):
		return "{}, {}, {}, {}, {}".format(self.member,self.string,self.total_before, self.total_after, self.impact )

class Visit(models.Model):	
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	ip = models.CharField(max_length=100)
	port = models.CharField(max_length=40)	
	time = models.DateTimeField(default= datetime.now)
	hasDon= models.BooleanField(default=False)
	
	def __str__(self):
		return "{},{},{},{},{}"(self.ip, self.port, self.time, self.user.first_name, self.hasDon)

#TODO: This needs Campaign as a FK here as well
class ChallengeLink(models.Model):
    challenger = models.ForeignKey(settings.AUTH_USER_MODEL, primary_key= True)
    challengee = models.ForeignKey(settings.AUTH_USER_MODEL, primary_key= True)
    pledge = models.TextField()

    def __str__(self):
    	return "Challenger:{}, Challengee:{}, Pledge:{}".format(self.challenger,\
    	 self.challengee, self.pledge)


class Condition(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, primary_key= True)
    campaign = models.ForeignKey(Campaign, primary_key= True)
    pledge = models.TextField()
    resolved = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    changed_on = models.DateField(default=date.today)

    def __str__(self):
        return "User: {}, Campaign: {}, Pledge: {}, Resolved: {}".format(self.user.first_name,\
         self.campaign.title , self.pledge, self.resolved)


class Membership(models.Model):
	group_name  = models.CharField(max_length=40, primary_key=True)
	member = models.CharField(max_length=40, primary_key=True)
	def __str__(self):
		return "Member: {}, Group: {}".format(self.member,self.group_name)


class Identifier(models.Model):
	name  = models.CharField(max_length=60, primary_key=True)
	category = models.CharField(max_length=40)

	def __str__(self):
		return "Name: {}, category: {}".format(self.name,self.category)
