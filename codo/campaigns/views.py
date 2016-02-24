import os
from django.conf import settings
from django.core import serializers 
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from formtools.preview import FormPreview
from formtools.wizard.views import SessionWizardView, NamedUrlSessionWizardView
from .models import Campaign, Organizer, Reward
from .forms import CampaignInfoForm,UserConditionalsForm, RewardFormSet,\
                    AccountInfoForm

User = get_user_model()



FORMS = [("campaign_info", CampaignInfoForm),
         ("user_conditionals", UserConditionalsForm),
         ("rewards", RewardFormSet),
         ("account_info", AccountInfoForm)]


TEMPLATES = {"campaign_info": "campaigns/campaign_info.html",
             "user_conditionals": "campaigns/user_conditionals.html",
             "rewards": "campaigns/rewards.html",
             "account_info": "campaigns/account_info.html"}


class CreateCampaign(NamedUrlSessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    def done(self,form_list, form_dict,**kwargs):
        account_info = form_dict['account_info']
        campaign_info = form_dict['campaign_info']
        #ToDo: Since it is possible that the user has not enabled conditionals
        # and/or rewards,first test if they exist (using get()) before trying to 
        # access them
        user_conditionals = form_dict['user_conditionals']
        rewards = form_dict['rewards']

        conditionals = user_conditionals.cleaned_data
        existing_organizer = Organizer.objects.filter(user=self.request.user)
        if len(existing_organizer) == 0:
            organizer = account_info.save(commit=False)
            organizer.user = self.request.user
            organizer.save()
        else:
            organizer = existing_organizer[0]

        campaign = campaign_info.save(commit=False)
        campaign.organizer = organizer
        campaign.friends_participation_cond = conditionals['friends_participation_cond']
        campaign.friends_participation_amount_cond = conditionals['friends_participation_amount_cond']
        campaign.community_participation_cond = conditionals['community_participation_cond']
        campaign.community_participation_amount_cond = conditionals['community_participation_amount_cond']
        campaign.milestone_cond = conditionals['milestone_cond']
        campaign.matching_donation_cond = conditionals['matching_donation_cond']
        campaign.save()

        new_rewards = rewards.save(commit=False)
        for reward in new_rewards:
            reward.campaign = campaign
            reward.save()
        #new_rewards.save()
        return redirect('/campaigns/'+str(campaign.id))

def show_reward_form(wizard):
    # try to get the cleaned data of step 1
    cleaned_data = wizard.get_cleaned_data_for_step('campaign_info') or {}
    # check if the field ``enable reward`` was checked.
    return cleaned_data.get('rewards_enabled', True)

def show_conditionals_form(wizard):
    # try to get the cleaned data of step 1
    cleaned_data = wizard.get_cleaned_data_for_step('campaign_info') or {}
    # check if the field ``enable reward`` was checked.
    return cleaned_data.get('conditionals_enabled', True)

class CampaignFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        return redirect('/')



def home(request):
    return render(request, "campaigns/index.html")

def campaigns(request, id=0):
    if id == 0:
        campaigns = serializers.serialize("json", Campaign.objects.all())
        return HttpResponse(campaigns)
    else:
        campaign = get_object_or_404(Campaign,id=int(id))
        rewards = campaign.reward_set.all()
        return render(request,"campaigns/campaign_page.html",\
         {'campaign':campaign, 'rewards': rewards})

    
def all_projects(request):
    return render(request, "campaigns/all_projects.html")


