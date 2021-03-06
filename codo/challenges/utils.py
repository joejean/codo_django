from django.http import JsonResponse, HttpResponseBadRequest
from .models import AmountLog, Log, Visit, ChallengeLink, Condition,\
					 Membership,Identifier
from django.contrib.auth import get_user_model


def logAmount(ip,port,user,campaign,amount,challenges):
	'''@param campaign is a campaign id'''
	amount_log = AmountLog.objects.create(ip=ip, port=port, user=user,campaign_id=campaign,
		amount=amount, challenges=challenges)

#Helper functions used in other apps
#This can be refactored later
def campaign_stats(campaign):
	'''Get Statistics about Current Campaign
	Params: campaigns: campaign id
	Returns:
		Amount Funded, Number of Funders, Number of Challenges
	'''
	total = currentTotal(campaign)
	num_funders = nResolvedConditions(campaign)
	num_challenges = nUnresolvedConditions(campaign)
	return total, num_funders, num_challenges

#This replaces the server class from the old codebase
#TODO: Misleading name, change name
def get_user_challenges_info(user,campaign):
	if user.is_authenticated():
		hasDon, donCon, donAmt, impact = hasDonation(user, campaign)
	else:
		hasDon = donCon = ""
		donAmt = impact = 0
	return hasDon, donCon, donAmt, impact
	# return JsonResponse({
	# "user":user.username,
	# "has_donation":str(hasDon).lower(),
	# "donation_amt":donAmt,
	# "impact":impact,
	# "donation_condition":donCon,
	# })

#Get Challenges for a User
def checkChallengeString(user):
	'''Get all standing challenges for a user for all campaigns'''
	relevant =  Condition.objects.filter(pledge__icontains=" "+user+" ").filter(resolved=0.0)
	# for row in Membership.objects.filter(member=user.username):
	# 	group = row.group_name
	# 	relevant.filter(pledge__icontains(user.username),pledge__icontains(group))
	#result = {"challenge":[dict(zip(['name', 'pledge'],[row.user.username, row.pledge])) for row in relevant]}
	return relevant

# return <true/false, donation string, resolved?>
def hasDonation(user, campaign):
	row = Condition.objects.filter(user=user, campaign=campaign).first()
	impactrow = Log.objects.filter(user=user, campaign=campaign).first()
	return (True, row.pledge, row.resolved, impactrow.impact if impactrow else 0) if row else (False, '', 0, 0)

def get_user_from_email(email):
	User = get_user_model()
	return User.objects.filter(email=email)[0]

def get_full_name(user):
	return user.first_name +" "+user.last_name

def logVisit(ip, port, user, system, hasDon):
	visit = Visit(ip=ip, port=port, user=user, system=system, hasDon=hasDon)
	visit.save()

def addMember(name):
	identifier = Identifier(name=name,category='member')
	identifier.save()

def makeGroup(name):
	identifier = Identifier(name=name,category='group')
	identifier.save()

def addToGroup(name, group):
	group = Identifier.objects.filter(name=group).first()
	if group is None:
		makeGroup(group)
	member = Identifier.objects.filter(name=name).first()
	if member is None:
		addMember(name)
	membership = Membership(member=name, group_name=group)
	membership.save() 

def addCondition(user, pledge,campaign):
	member = Identifier.objects.filter(name=user.username).first()
	if member is None:
		addMember(user.username)
	condition = Condition.objects.create(user=user, pledge=pledge, campaign_id=campaign)
	


def addChallengeLinks(challenger,challengees, condition, campaign):
	'''
		@param challengees : comma separated string of usernames.
		@param challenger: user object
	'''
	member = Identifier.objects.filter(name=challenger.username)
	if not member:
		addMember(challenger.username)
	for challengee in challengees.split(','):
		member = Identifier.objects.filter(name=challengee)
		if not member:
			addMember(challengee)
		challenge_link = ChallengeLink.objects.create(challenger=challenger.username, challengee=challengee, pledge=condition,campaign_id=campaign)
		
		

def param_error(param):
	'''Helper function to return an error message when a required
	   parameter is missing from the POST request data.
	'''
	return HttpResponseBadRequest("please provide the {} parameter in a variable called '{}'.".format(param, param))

def currentTotal(campaign):
	resolved_conditions = Condition.objects.exclude(resolved=0).filter(campaign=campaign) 
	result = sum([float(x.resolved) for x in resolved_conditions ])
	return result

def nResolvedConditions(campaign):
	result = Condition.objects.exclude(resolved=0).filter(campaign=campaign)
	return len(result)

def nUnresolvedConditions(campaign):
	result = Condition.objects.filter(resolved=0, campaign=campaign)
	return len(result)

