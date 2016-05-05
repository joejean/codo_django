from django.conf import settings 
import string, random, subprocess, re, time
from .models import AmountLog, Log, Visit, ChallengeLink, Condition,\
                     Membership,Identifier

CPLEX_OUTPUT_PATH = settings.CPLEX_OUTPUT_PATH
CPLEX_INSTALL_PATH = settings.CPLEX_INSTALL_PATH

original = """\ENCODING=ISO-8859-1
\Problem name: 

Maximize
[objective]
Subject To
[constraints]

Bounds
[bounds]

General
[generals]
End"""


def isFloatable(string):
    try:
        float(string)
        return True
    except:
        return False

# Takes as input a condition string "100 if Jay > 50" and returns the x, y and x_max linear equations/values
def parseCondition(name, conditions):
    # Matching donations 
    if "MATCH" in conditions.split(' '):
        terms = conditions.split(' ')
        ratio = terms[1].split(':')
        percent = float(ratio[0])/float(ratio[1])
        x_max = terms[terms.index("LIMIT")+1]

        # Group Matching
        if "FROM" in terms:
            target = terms[terms.index("FROM")+1]

        # Individual Matching
        else:
            target = terms[2]

        y = ["<y_%s>"%(target)]
        x = str(percent)+" <xy_%s>"%(target)
        if len(terms) > terms.index("LIMIT")+2 :
            conditions = terms[terms.index("LIMIT")+2:]
        else:
            return (x, x_max, y) 
        

    else:
        x = conditions.split(' ')[0]
        x_max = x
        y = []


    # Catch regular donations
    if len(conditions.split(' ')) == 1:
        y = ['1']
        return (x, x_max, y)


    # List of conditional statements "Jay" "Group" "10 People"
    for condition in [a.strip() for a in ' '.join(conditions.split(' ')[2:]).split("AND")]:
        # Tags in the form <identifier_variable> are to be resolved later
        terms = condition.split(' ')

        # Simple donations "Jay" or "Group"
        if len(terms) == 1:
            y.append( "<y_%s>"%(terms[-1]) )


        # Catch global N-People Conditionals
        elif "PEOPLE" in terms:
            n_people = int(terms[terms.index("PEOPLE")-1])

            if "HAS" in terms:
                group = terms[0]
                if terms[-1] == "PEOPLE":
                    y.append( str("{0}".format(1.0/n_people))+" <y_%s~%s>"%(group, name) )
                else:
                    y.append( str("{0}".format(1.0/n_people))+" <z%s_%s~%s>"%(terms[-1],group,name) )

            else:
                if terms[-1] == "PEOPLE":
                    y.append( str("{0}".format(1.0/n_people))+" <y_everyone~%s>"%(name) )
                else:
                    y.append( str("{0}".format(1.0/n_people))+" <z%s_everyone~%s>"%(terms[-1],name) )


        # Catch Percentage on Group
        elif condition[-1]=="%":
            y.append( "<!MATH! 1/%s_len * %s>"%(group,float(terms[-1].strip("%")))  +  " <y_%s>"%(terms[0]) )


        # Catch Group / Individual SUM donation
        elif "HAS" in terms:
            y.append( str(1/float(terms[-1]))+" <xy_%s>"%(terms[0]) )

    return (x, x_max, y) if y else None

def cleanEquation(eq):
    leftSide, comp, rightSide = re.split("(<=|>=)",eq)
    variables = [x for x in re.findall(ur'(?P<sign>[\+|-]?)\s?(?P<scalar>[0-9\.]*)\s?(?P<variable>[A-z_0-9]*)',leftSide) if any(x)]
    newLeft = []
    newRight = float(rightSide)
    for v in variables:
        if v[0] and v[1] and not v[2]:
            newRight-=float(''.join(v))
        else:
            newLeft.append(' '.join(v).strip())
    newRight = int(newRight) if not newRight % 1 else newRight
    return " ".join([' '.join(newLeft), comp, str(newRight)])


class Scenario:
    def __init__(self):
        self.filename = 'cplex_'+str(time.time())+str(random.randint(100,999))+'.lp'
        self.groups =       {}
        self.bounds =       set()
        self.constraints =  set()
        self.xyBank =       set()
        self.zedBank =      set()   

    def includeDonation(self,name,donationString):
        self.observeConditional(name, *parseCondition(name,donationString))

    def observeConditional(self, name, x, x_max, ys):
        # Define Variable names - x_Name, y_Name, xy_Name
        x_var, y_var ,xy_var= "x_" + name , "y_" + name , "xy_" + name

        # Log the presence of the XY for the rest of the system
        # It case it doesn't already exist
        self.xyBank.add(xy_var)
        
        # x <= value
        self.constraints.add(x_var + " <= " + str(x))
        
        # y - condition <= value
        for y in ys:
            if isFloatable(y):
                self.constraints.add(y_var + " <= "+ str(y))
            else:
                self.constraints.add(y_var  + " - " + str(y)+ " <= 0")

        # y <= 1
        self.bounds.add("0 <= " + y_var  + " <= 1")

        # xy - Max(x) * y <= 0
        self.constraints.add(xy_var + " - " + str(x_max) + " " + y_var + " <= 0")

        # xy - x <= 0
        self.constraints.add(xy_var + " - " + x_var + " <= 0" )

        # xy - x - max(x) * y >= - max(x)
        self.constraints.add(xy_var + " - " + x_var + " - " + str(x_max) +" " + y_var + " >= -"+str(x_max))

        # 0 <= xy
        self.bounds.add("0 <= " + xy_var)

        # x <= Max(x)
        self.bounds.add(x_var + " <= " + str(x_max))

        # xy <= x
        self.bounds.add(xy_var + " <= " + str(x_max))


    def finalizeGroups(self):
        members = reduce(lambda x,y: x|y, self.groups.values())
        self.groups.update({name:set([name]) for name in members})
        self.groups['everyone'] = set(members)

    def expandTags(self):
        p = re.compile(ur'(?P<sign>\+|-)\s?(?P<scalar>[0-9\.]*)\s?<(?P<variable>[A-z]+)(?P<amount>[0-9]*)_(?P<identifier>.+)>')
        newSet = set()
        for eq in self.constraints:
            result = re.search(p, eq)
            # No markup in equation
            if not result:
                newSet.add(eq)
            # Markup found in equation 
            else:
                # Isolate full tag context
                tag = result.group(0)

                # Select exclusionary groups
                if "~" in result.group('identifier'):
                    members = self.groups[result.group('identifier').split("~")[0]] - set([result.group('identifier').split("~")[1]])

                # Leave unclaimed names be
                elif result.group('identifier') not in self.groups.keys():
                    newSet.add(eq.replace(tag, result.group('sign')+" "+result.group('scalar').strip() +" "+ result.group('variable')+ result.group('amount')+"_"+result.group('identifier')))
                    continue

                # If normal markup - fetch members
                else:
                    members = self.groups[result.group('identifier')]

                # Expand markup equation 
                expansion = ' '.join([ (result.group('sign')+" "+result.group('scalar')).strip() +" "+ result.group('variable')+ result.group('amount')+"_"+member.email for member in members ])
                newSet.add(eq.replace(tag,expansion))

                if result.group("variable") == "z":
                    [self.zedBank.add(member.email+"|z|"+result.group("amount")) for member in members]
        self.constraints = newSet

    def makeZeds(self):
        for z in self.zedBank:
            name,_,threshold= z.split("|") 
            z_var = "z"+threshold+"_"+name
            xy_var = "xy_"+name
            self.constraints.add(z_var + " - " + str("{0}".format(1.0/(float(threshold)))) + " " + xy_var + " <= 0")
            self.bounds.add(z_var + " <= 1")

    def fillBlanks(self):
        variables = set(re.findall(ur'[A-z]+[0-9]*_[A-z0-9]*', "\n".join(list(self.constraints)+list(self.bounds))))
        users = set([var.split("_")[1] for var in self.xyBank])
        [self.bounds.add(var+" = 0") for var in variables if var.split("_")[1] not in users]

    def solveLP(self):
        template = original.replace("[constraints]","\n".join(["   C"+str(i)+": "+constraint for i, constraint in enumerate(sorted(list(self.constraints), key= lambda x: x.split('_')[1]))]))
        template = template.replace("[objective]","   obj:  "+ " + ".join(sorted(list(self.xyBank))))
        template = template.replace( "[bounds]","   "+ "\n   ".join(sorted(list(self.bounds), key= lambda x: x.split('_')[1])))
        template = template.replace("[generals]","\t"+"\n\t".join(sorted(["z"+z.split("|")[2] +"_"+z.split("|")[0] for z in self.zedBank]+map(lambda x: x.replace('xy_',"y_"),list(self.xyBank)))))
        f = open(CPLEX_OUTPUT_PATH+self.filename,'w')
        f.write(template)
        f.close()
        readout = subprocess.check_output([CPLEX_INSTALL_PATH+' -c "read "'+CPLEX_OUTPUT_PATH+'"%s" "optimize"  "display solution objective" "display solution variables -"'%(self.filename)],shell=True).strip().split('\n')
        try:
            solution = map(lambda x: (x[0].split("_")[1],float(x[1])),[filter(None, x.split(' ')) for x in  readout[readout.index('CPLEX> Incumbent solution')+2:-1] if "xy_" in x])
        except ValueError:
            solution = []
            print readout
        for xy in self.xyBank:
            if xy not in ["xy_"+x[0] for x in solution]:
                solution.append((xy.split("_")[1],0.0))
        total = reduce(lambda x,y: ('total',x[1]+y[1]), solution) if len(solution)>1 else ('total',solution[0][1])
        return solution + [total]

    def packAndSolve(self):
        if len(self.constraints) == 0:
            return [('total',0.0)]
        self.finalizeGroups()
        self.expandTags()
        self.makeZeds()
        self.fillBlanks()
        result = self.solveLP()
        subprocess.call(['rm '+CPLEX_OUTPUT_PATH+self.filename],shell=True)
        print("PACKANDSOLVE RESULTS")
        print(result)
        return result


    
    #TODO: Need to modify this to take the campaign into account
    def populateFromDB(self):
        groups = Identifier.objects.filter(category="group")
        for g in groups:
            self.groups[g.name]=set()
            for m in Membership.objects.filter(group_name=g.name):
                self.groups[g.name].add(m.member)
        members = Identifier.objects.filter(category="member")
        for member in members:
            self.groups[member.name] = set([member.name])
        #TODO: Add Campaign support here
        conditions = Condition.objects.all()
        for c in conditions:
            self.includeDonation(c.user.email,c.pledge)
        

def runTest():
    testScenario = Scenario()

    for member in sample_members[:2]:
        sample = random.choice([c for c in sample_conditions if "<group>" not in c])
        if "<member>" in sample:
            sample = sample.replace("<member>", random.choice(filter(lambda x: x!=member,sample_members)))
        if "<group>" in sample:
            sample = sample.replace("<group>", random.choice(sample_groups))

        print member, sample
        testScenario.includeDonation(member, sample)


    for g in sample_groups:
        testScenario.groups[g] = set()
        for i in range(10):
            testScenario.groups[g]|=set([random.choice(sample_members)])

    print testScenario.packAndSolve()


