from django.http import JsonResponse, HttpResponseBadRequest
from .models import AmountLog, Log, Visit, ChallengeLink, Condition,\
					 Membership,Identifier
from django.contrib.auth import get_user_model

def logAmount(ip,port,user,campaign,amount,challenges):
	'''@param campaign can be a campaign id or a campaign object'''
	amount_log = AmountLog(ip=ip, port=port, user=user,campaign=campaign,
		amount=amount, challenges=challenges)
	amount_log.save()


# def submitSurvey(survey):
#     session=Session()
#     session.merge(Survey(*survey))
#     session.commit()
#     session.close()


def get_user_from_username(username):
	User = get_user_model()
	return User.objects.filter(username=username)[0]

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
	condition = Condition(user=user, pledge=pledge, campaign=campaign)
	condition.save()


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
		challenge_link = ChallengeLink(challenger=challenger.username, challengee=challengee, condition=condition,campaign=campaign)
		challenge_link.save()
		

def param_error(param):
	'''Helper function to return an error message when a required
	   parameter is missing from the POST request data.
	'''
	return HttpResponseBadRequest("please provide the {} parameter in a variable called '{}'.".format(param, param))