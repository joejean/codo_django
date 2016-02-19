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
from .models import Campaign, Organizer
from .forms import CampaignInfoForm,UserConditionalsForm, RewardForm,\
                    AccountInfoForm

User = get_user_model()


FORMS = [("campaign_info", CampaignInfoForm),
         ("user_conditionals", UserConditionalsForm),
         ("rewards", RewardForm),
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
        new_rewards.campaign = campaign
        new_rewards.save()
        return redirect('/')

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
        return render(request,"campaigns/campaign_page.html", {'campaign':campaign})



    
def all_projects(request):
    return render(request, "campaigns/all_projects.html")

@login_required(login_url='/accounts/login')
def create_campaign(request):
    if request.method == 'POST':
        if 'campaign_name' in request.POST:
            campaign_name = request.POST['campaign_name']
        if 'campaign_description' in request.POST:
            campaign_description = request.POST['campaign_description']
        if 'campaign_picture_url' in request.POST:
            campaign_picture_url = request.POST['campaign_picture_url']
        if 'campaign_video_url' in request.POST:
            campaign_video_url = request.POST['campaign_video_url']
            #TODO: Make Sure the user is an organizer
        campaign = Campaign.objects.create(organizer_id=request.user.id, name=campaign_name, 
            description=campaign_description, video_url=campaign_video_url, 
            picture_url=campaign_picture_url)
        return redirect('/')
    return render(request, 'campaigns/create_campaign.html')

