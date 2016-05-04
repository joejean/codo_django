from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from .solver import * 
from .models import AmountLog, Log, Visit, ChallengeLink, Condition,\
					 Membership,Identifier
from .utils import logAmount, logVisit, addMember, makeGroup, addToGroup,\
					addCondition, addChallengeLinks, param_error, get_user_from_email,\
					hasDonation
from ipware.ip import get_real_ip
from copy import deepcopy
import sys


#This replaces the server class from the old codebase
# def user_challenges_info(request):
# 	if request.method == 'POST':
# 		campaign = request.POST.get('campaign')
# 		if campaign is None:
# 			return param_error("campaign")
# 		hasDon, donCon, donAmt, impact = hasDonation(request.user, campaign)
# 		return JsonResponse({
# 		"user":request.user.email,
# 		"has_donation":str(hasDon).lower(),
# 		"donation_amt":donAmt,
# 		"impact":impact,
# 		"donation_condition":donCon,
# 		})

def rippler(request):
	if request.method == "POST":
		ip = get_real_ip(request)
		if ip is None:
			ip = "0.0.0.0"
		#TODO: Change this to make it take a real port number	
		port = "80"
		action = request.POST.get('action')

		#TODO: Remove this
		# if action == "requestLogin":
		#     netID = request['netID']
		#     system = 'test'
		#     return JsonResponse({'recipient':makeLogin(netID,system)})

		if action == "hasDonation":
		# return <true/false, donation string, resolved?>
			campaign = request.POST.get('campaign')
			if campaign is None:
				return param_error("campaign")
			return JsonResponse(hasDonation(request.user, campaign))

		# Query for project statistics (current funded, goal, number of users resolved, number of users unresolved)
		if action == "getProjectStats":
			campaign = request.POST.get('campaign')
			if campaign is None:
				return param_error("campaign")
			return JsonResponse({"amt_funded":currentTotal(campaign), "num_funders":nResolvedConditions(campaign), "num_challenges":nUnresolvedConditions(campaign)})

		# Query for still-standing challenges/conditions (unresolved)
		if action == "prevChallenges":
			campaign = request.POST.get('campaign')
			if campaign is None:
				return param_error("campaign")
			return JsonResponse({"challenges": listUnresolvedConditions(campaign)})

		# Query for resolved user, amount tuples
		if action == "prevDonations":
			campaign = request.POST.get('campaign')
			if campaign is None:
				return param_error("campaign")
			return JsonResponse({"donations":lastNResolved(int(request.POST.get('n')),campaign)})

		# Query for suggested donation returns list of good ratio points
		if action == "getHighImpactPoints":
			user = request.user 
			highest = int(request.POST.get("highest"))
			lowest = int(request.POST.get("lowest"))
			stepsize = int(request.POST.get("stepsize"))
			return JsonResponse({"impactPoints":highestImpact(user, lowest, highest, stepsize)})

		# Query for hypothetical or process donation
		if action == "processDonation":
			user = request.user
			donation = request.POST.get('donation')
			campaign = int(request.POST.get('campaign'))
			before, after, change = changeBetween(beforeAfter(user, donation))
			nChallenges = len([k for k in change.keys() if k!='total' and change[k]>0])
			if all([letter in string.digits+'.' for letter in donation]) and len(donation)>0: logAmount(ip,port,user,campaign,float(donation),nChallenges)
			print after
			impact = change['total']-after[user.email]
			percent = impact/after[user.email] * 100 if after[user.email] else 0
			if request.POST.get('state') == "submit":
				
				submitDonation(request.user, request.POST['campaign'],request.POST['donation'])
				if request.POST.get('challengees') != '':
					addChallengeLinks(request.user,request.POST['challengees'],request.POST['donation'],request.POST['campaign'])
			return JsonResponse({"before":before, "after":after, "change":change, "impact": impact, "percent": percent })

		# List all users
		if action == "listUsers":
			return JsonResponse({"users":[row.name for row in getMembers()]})

		# Get all standing challenges for a user for all campaigns
		if action == "checkForChallenges":
			user = request.user
			return JsonResponse(checkChallengeString(user))

		# Get all standing challenges for a user for a given campaign
		if action == "checkCampaignChallenges":
			campaign = request.POST.get('campaign')
			if campaign is None:
				return param_error("campaign")
			user = request.user
			return JsonResponse(checkCampaignChallenges(user, campaign))

		if action == "getNetwork":
			user = request.user
			campaign = request.POST.get('campaign')
			if campaign is None:
				return param_error("campaign")
			return JsonResponse({'links':getNetwork(user, campaign)})

		if action == "getRipples":
			user = request.user
			highest = int(request.POST.get("highest"))
			lowest = int(request.POST.get("lowest"))
			stepsize = int(request.POST.get("stepsize"))
			return JsonResponse(getRipples(user,lowest,highest,stepsize))

		if action == "getFullNetwork":
			return JsonResponse(getFullNetwork())

def sanitize(someString):
	return ''.join([letter for letter in someString if letter in string.letters+string.digits+string.whitespace])


#TODO: This should be deleted
# def getSystem(user):
	
#     result = session.query(Login).filter(Login.name==user).first()
   
#     return result.system if result else None

#This function does not seem to be used anywhere
def logBalance():
	logs = session.query(Login).all()
	sys_variables = [log.system for log in logs]
	result = {var:sys_variables.count(var) for var in set(sys_variables+['control','test'])}
	return result

def getMembers():
	result = Identifier.objects.filter(category="member")
	return result


def getNetwork(user, campaign):
	links = ChallengeLink.objects.filter(Q(challenger=user.email) | Q(challengee=user.email))
	lines = links.filter(campaign=campaign)
	result = [{'challenger':row.challenger, 'challengee':row.challengee, 'condition':row.pledge} for row in lines]
	return result

def checkChallengeString(user):
	'''Get all standing challenges for a user for all campaigns'''
	relevant =  Condition.objects.none()
	for row in Membership.objects.filter(member=user.email):
		group = row.group_name
		relevant.filter(pledge__icontains(user.email),pledge__icontains(group))
	result = {"challenge":[dict(zip(['name', 'pledge'],[row.name, row.pledge])) for row in relevant]}
	return result

def checkCampaignChallenges(user, campaign):
	'''Check for user challenges in a particular campaign'''
	relevant =  Condition.objects.none()
	for row in Membership.objects.filter(member=user.email):
		group = row.group_name
		relevant.filter(pledge__icontains(user.email),pledge__icontains(group),campaign=campaign)
	result = {"challenge":[dict(zip(['name', 'pledge'],[row.name, row.pledge])) for row in relevant]}
	return result


def getRipples(user,lowest,highest,stepsize):
	before = Scenario()
	before.populateFromDB() 
	after  = deepcopy(before)
	after.groups[user]=set([user])
	active_before = before.packAndSolve()
	activation_points = {}
	for i in range(lowest,highest,stepsize):
		tempState = deepcopy(after)
		tempState.includeDonation(user.email,str(i))
		b, a, c = changeBetween((active_before,tempState.packAndSolve()))
		realChange = [(key,a[key]) for key in a.keys() if a[key]!=0 and key in b.keys() and a[key]!=b[key]]
		for u, amount in realChange:
			if u in [user, 'total']:
				continue
			if u not in activation_points.keys():
				activation_points[u] = {}
			if amount not in activation_points[u].keys():
				activation_points[u][amount] = i
	return activation_points


def nResolvedConditions(campaign):
	result = Condition.objects.exclude(resolved=0).filter(campaign=campaign)
	return len(result)

def nUnresolvedConditions(campaign):
	result = Condition.objects.filter(resolved=0, campaign=campaign)
	return len(result)

def currentTotal(campaign):
	resolved_conditions = Condition.objects.exclude(resolved=0).filter(campaign=campaign)
	result = sum([x[0] for x in resolved_conditions ])
	return result

def listUnresolvedConditions(campaign):
	unresolved = Condition.objects.filter(resolved=0, campaign=campaign)
	result = [item.user.email + " " + item.pledge for item in unresolved]
	return result

def lastNResolved(n, campaign):
	result = Condition.objects.exclude(resolved=0).filter(campaign=campaign).order_by('-changed_on')[:n]
	return [{'name':row.user.email, 'donation': row.resolved} for row in result] 

def lastNUnresolved(n, campaign):
	result = Condition.objects.filter(resolved=0,campaign=campaign).order_by('-changed_on')[:n]
	return result




#TODO: Special Attention
def markThoseResolved(campaign):
	scenario = Scenario()
	scenario.populateFromDB()
	active = filter(lambda x: x[0]!='total',scenario.packAndSolve())
	for name, amount in active:
		condition, created = Condition.objects.get_or_create(user=get_user_from_email(name), campaign=campaign)
		if not condition:
			continue
		if condition.resolved != amount:
			condition.resolved = amount
			condition.changed_on = func.now()
			condition.save()
	
#TODO: Need to modify this to take the campaign into account
def submitDonation(user,campaign,donation):
	before, after, change = changeBetween(beforeAfter(user, donation))
	addCondition(user,donation,campaign)
	log, created = Log.objects.update_or_create(user=user, campaign_id=campaign,
	 pledge=donation, total_before=before['total'], total_after=after['total'],
	 impact=change['total'] - after[user.email]) 
	markThoseResolved(campaign)
	return after

def beforeAfter(user, donation):
	before = Scenario()
	before.populateFromDB()
	after  = deepcopy(before)
	after.groups[user.email]=set([user.email])
	after.includeDonation(user.email, donation)
	b = before.packAndSolve()
	a = after.packAndSolve()
	return b, a

def changeBetween(beforeAndAfter):
	before, after = beforeAndAfter
	b = dict(before)
	a = dict(after)
	c = dict()
	for name in a.keys():
		c[name] = a[name] - b[name] if name in b.keys() else a[name]
	return b, a, c


def highestImpact(user,lowest,highest,stepsize):
	before = Scenario()
	before.populateFromDB() 
	after  = deepcopy(before)
	after.groups[user.email]=set([user.email])
	prevTotal = dict(before.packAndSolve())['total']
	ratios = []
	for i in range(lowest,highest,stepsize):
		tempState = deepcopy(after)
		tempState.includeDonation(user.email,str(i))
		tempTotal = dict(tempState.packAndSolve())['total']
		tempImpact = tempTotal - prevTotal - i
		ratios.append((i,100*tempImpact/float(i), tempImpact))
	sortedRatios = sorted(ratios, key=lambda x: x[1], reverse=True)
	junk = []
	for i in range(1,len(sortedRatios)):
		if sortedRatios[i-1][0] + stepsize == sortedRatios[i][0]:
			junk.append(sortedRatios[i])
	[sortedRatios.remove(j) for j in junk]
	return [dict(zip(['amount','impact','percent'],row)) for row in sortedRatios]

#NOTE: This does not seem to be used
def replicateConditions():
	logs = Log.objects.all()
	conditions = [(str(row.user.email),str(row.pledge)) for row in logs]
	return conditions

#TODO: Test to see if it works
def getFullNetwork(campaign):
	users = Identifier.objects.filter(category='member')
	network = []
	for useremail in users:
		donation = Condition.objects.filter(user=get_user_from_email(useremail), campaign=campaign).first()
		if donation:
			pledge = donation.pledge
			resolved = int(donation.resolved)
			max_donation = int(pledge.split(' ')[0] if 'MATCH' not in pledge else pledge.split(' ')[-1])
		else:
			pledge = None
			resolved = 0
			max_donation = 0
		personal_Network = getNetwork(user.email, campaign)
		challengers, challengees = [], []
		for node in personal_Network:
			#TODO: Check to see if challenger here returns a user object or a username
			if node['challenger'] != username:
				challengers.append(node['challenger'])
			if node['challengee'] != username:
				challengees.append(node['challengee'])
		network.append({'username': username, 'max_donation': max_donation, 'resolved': resolved, 'condition': pledge,  'challenging': challengees, 'challenged_by': challengers})
	relevant_network = []
	for node in network:
		relevant = True
		if node['resolved']==node['max_donation']:
			relevant = False
			for neighbor in node['challenged_by']+node['challenging']:
				for node in network:
					if node['username']==neighbor and node['resolved']!=node['max_donation']:
						relevant = True
						break
				if relevant: break
		if relevant:
			relevant_network.append(node)
	return relevant_network

#TODO: REMOVE
# def authenticate(user, password):
#     
#     login = session.query(Login).filter(Login.name==user).first()
#     if login and login.password==password:
#         return True
#     else:
#         return False

#TODO: Look into this
# def makeRandomDonation(member):
#     sample = random.choice([c for c in sample_conditions if "<group>" not in c])
#     target = None
#     if "<member>" in sample:
#         target = random.choice(filter(lambda x: x!=member,sample_members))
#         sample = sample.replace("<member>", target)
#     if "<group>" in sample:
#         sample = sample.replace("<group>", random.choice(sample_groups))
#     for i in range(sample.count("<amount>")):
#         sample = sample.replace("<amount>", str(random.choice(range(5,60,5))),1)
#     if "<population>" in sample:
#         sample = sample.replace("<population>", str(random.randint(2,40)))
#     if "<percent>" in sample:
#         sample = sample.replace("<percent>", str(random.randint(10,100)))

#     print member, sample
#     if target: addChallengeLinks(member, target, sample)
#     submitDonation(member, sample, random.choice(['fake']))

#TODO: Remove
# def loadSample():
#     random.shuffle(sample_members)
#     for member in sample_members[:50]:
#         makeRandomDonation(member)

#TODO: Remove 
# if __name__ == '__main__':
#     if len(sys.argv) != 2:
#         print 'Loading up dummy data onto database - to actually start a server provide a port number in the commandline'
#         loadSample()
#     else:
#         app = web.application(urls, globals())
#         app.run()
		
