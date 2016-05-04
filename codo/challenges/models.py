from datetime import date, datetime
from django.db import models
from django.conf import settings
from campaigns.models import Campaign

class AmountLog(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	campaign = models.ForeignKey(Campaign)
	ip = models.CharField(max_length=100)
	port = models.CharField(max_length=40)	
	time = models.DateTimeField(default= datetime.now)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	challenges = models.IntegerField()
	
	def __str__(self):
		return "{}, {}, {}, {}, {}, {}".format(self.ip,self.port,self.time,self.user.username,self.amount,self.challenges)
		
class Log(models.Model):
	campaign = models.ForeignKey(Campaign)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	submitted_on = models.DateTimeField(default= datetime.now)
	pledge = models.TextField()
	total_before = models.DecimalField(max_digits=15, decimal_places=2)
	total_after = models.DecimalField(max_digits=15, decimal_places=2)
	impact = models.DecimalField(max_digits=15, decimal_places=2)

	def __str__(self):
		return "{}, {}, {}, {}, {}".format(self.campaign.title,self.user.username,self.total_before, self.total_after, self.impact )

class Visit(models.Model):	
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	ip = models.CharField(max_length=100)
	port = models.CharField(max_length=40)	
	time = models.DateTimeField(default= datetime.now)
	hasDon= models.BooleanField(default=False)
	
	def __str__(self):
		return "{},{},{},{},{}"(self.ip, self.port, self.time, self.user.username, self.hasDon)


class ChallengeLink(models.Model):
	'''Challenger and Challengee are both email addresses'''
	campaign = models.ForeignKey(Campaign)
	challenger = models.CharField(max_length=45)
	#models.ForeignKey(settings.AUTH_USER_MODEL, related_name="challenger_user")
	challengee = models.CharField(max_length=45)
	#models.ForeignKey(settings.AUTH_USER_MODEL, related_name="challengee_user")
	pledge = models.TextField()
	class Meta:
		#This is how we do a multiple column primary key in Django
		#see https://docs.djangoproject.com/en/1.8/ref/models/options/#unique-together
		unique_together = ('campaign', 'challenger', 'challengee')

	def __str__(self):
		return "Challenger:{}, Challengee:{}, Pledge:{}".format(self.challenger,\
		self.challengee, self.pledge)


class Condition(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	campaign = models.ForeignKey(Campaign)
	pledge = models.TextField()
	resolved = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
	changed_on = models.DateField(default=date.today)

	class Meta:
		#This is how we do a multiple column primary key in Django
		#see https://docs.djangoproject.com/en/1.8/ref/models/options/#unique-together
		unique_together = ('user', 'campaign')

	def __str__(self):
		return "User: {}, Campaign: {}, Pledge: {}, Resolved: {}".format(self.user.username,\
		 self.campaign.title , self.pledge, self.resolved)

#TODO: Do we need membership per campaign?
class Membership(models.Model):
	group_name  = models.CharField(max_length=40)
	member = models.CharField(max_length=40) # member is username
	class Meta:
		#This is how we do a multiple column primary key in Django
		#see https://docs.djangoproject.com/en/1.8/ref/models/options/#unique-together
		unique_together = ('group_name', 'member')

	def __str__(self):
		return "Member: {}, Group: {}".format(self.member,self.group_name)


class Identifier(models.Model):
	name  = models.CharField(max_length=60, unique=True)
	category = models.CharField(max_length=40)

	def __str__(self):
		return "Name: {}, category: {}".format(self.name,self.category)
