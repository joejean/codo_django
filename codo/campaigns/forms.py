from django import forms
from .models import Reward, Campaign


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class CampaignInfoForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'blurb', 'category', 'description', 'video_url',
         'picture', 'goal_amount', 'end_date', 'rewards_enabled','conditionals_enabled']

class UserConditionalsForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['friends_participation_cond', 'friends_participation_amount_cond',
            'community_participation_cond','community_participation_amount_cond',
            'milestone_cond', 'matching_donation_cond']
   
class RewardForm(forms.ModelForm):
     class Meta:
        model = Reward
        fields = ['title', 'pledge_amount', 'number_funders', 'description']

RewardFormSet = forms.formset_factory(RewardForm, extra=2)



   


