from .models import Amount_Log, Log, Visit, ChallengeLink, Condition,\
                     Membership,Identifier


def logAmount(ip,port,user,amount,challenges):
    amount_log = Amount_Log(ip=ip, port=port, user=user, amount=amount, challenges=challenges)
    amount_log.save()


# def submitSurvey(survey):
#     session=Session()
#     session.merge(Survey(*survey))
#     session.commit()
#     session.close()

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
#TODO: Change 'name' to 'email'
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
    member = Identifier.objects.filter(name=user.email).first()
    if member is None:
        addMember(user.email)
    condition = Condition(user=user, pledge=pledge, campaign=campaign)
    condition.save()

#Challengees is a comma separated string of emails.
#challenger is a user object
def addChallengeLinks(challenger,challengees, condition):
    member = Identifier.objects.filter(name=challenger.email)
    if not member:
        addMember(challenger.email)
    for challengee in challengees.split(','):
        member = Identifier.objects.filter(name=challengee)
        if not member:
            addMember(challengee)
        challenge_link = ChallengeLink(challenger=challenger.email, challengee, condition)
        challenge_link.save()
        