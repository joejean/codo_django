from django.contrib import admin
from .models import AmountLog, Log, Visit, ChallengeLink, Condition,\
					 Membership,Identifier
# Register your models here.
admin.site.register(AmountLog)
admin.site.register(Log)
admin.site.register(Visit)
admin.site.register(ChallengeLink)
admin.site.register(Condition)
admin.site.register(Membership)
admin.site.register(Identifier)





