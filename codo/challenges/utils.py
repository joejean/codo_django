from django.http import JsonResponse, HttpResponseBadRequest
from .models import AmountLog, Log, Visit, ChallengeLink, Condition,\
					 Membership,Identifier
from django.contrib.auth import get_user_model


def logAmount(ip,port,user,campaign,amount,challenges):
	'''@param campaign is a campaign id'''
	amount_log = AmountLog.objects.create(ip=ip, port=port, user=user,campaign_id=campaign,
		amount=amount, challenges=challenges)



# def submitSurvey(survey):
#     session=Session()
#     session.merge(Survey(*survey))
#     session.commit()
#     session.close()

#This replaces the server class from the old codebase
def get_user_challenges_info(user,campaign):
	hasDon, donCon, donAmt, impact = hasDonation(user, campaign)
	return hasDon, donCon, donAmt, impact
	# return JsonResponse({
	# "user":user.username,
	# "has_donation":str(hasDon).lower(),
	# "donation_amt":donAmt,
	# "impact":impact,
	# "donation_condition":donCon,
	# })

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