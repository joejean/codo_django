from django.contrib import admin
from .models import Reward, Campaign, Organizer
# Register your models here.

class CampaignAdmin(admin.ModelAdmin):
	fields = ( 'organizer','title', 'blurb','category','image_tag','description','video_url',
				'goal_amount', 'end_date', 'status', )
	readonly_fields = ('image_tag',)

class OrganizerAdmin(admin.ModelAdmin):
	fields = ( 'user','country','phone_number','profile_picture_tag','short_bio','facebook_url',
				'twitter_url','website_url','dob', )
	readonly_fields = ('profile_picture_tag',)

admin.site.register(Reward)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Organizer, OrganizerAdmin)

