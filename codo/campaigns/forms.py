from django import forms
from .models import Reward, Campaign, Organizer
from config import settings
from django_countries.widgets import CountrySelectWidget
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from bootstrap3_datetime.widgets import DateTimePicker


class BaseRewardFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseRewardFormSet, self).__init__(*args, **kwargs)
        self.queryset = Reward.objects.none()


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=60, label='First Name')
    last_name = forms.CharField(max_length=60, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class OrganizerInfoForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['country', 'phone_number', 'short_bio', 'profile_picture',
                    'facebook_url', 'twitter_url', 'website_url', 'dob']
        widgets = {
            'country': CountrySelectWidget(),
            'dob': DateTimePicker(options={"format": "YYYY-MM-DD",
                                            "pickTime": False})
        }

class CampaignInfoForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'blurb', 'category', 'description', 'video_url',
         'picture', 'goal_amount', 'end_date', 'rewards_enabled','conditionals_enabled']
        widgets = {
            'category': forms.widgets.Select(choices=[('art','Art'),('test','Test')]),
            'end_date': DateTimePicker(options={"format": "YYYY-MM-DD",
                                                "pickTime": False})  
        }

class UserConditionalsForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['friends_participation_cond', 'friends_participation_amount_cond',
            'community_participation_cond','community_participation_amount_cond',
            'milestone_cond', 'matching_donation_cond']
   
# class RewardForm(forms.ModelForm):
#      class Meta:
#         model = Reward
#         fields = ['title', 'pledge_amount', 'number_funders', 'description']

RewardFormSet = forms.modelformset_factory(Reward, exclude=('campaign',),\
    formset=BaseRewardFormSet)



   


