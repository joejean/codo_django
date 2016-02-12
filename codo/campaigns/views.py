import os
from django.conf import settings
from django.core import serializers 
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from formtools.preview import FormPreview
from formtools.wizard.views import SessionWizardView
from .models import Campaign
from .forms import CampaignInfoForm,UserConditionalsForm, RewardForm 

User = get_user_model()


FORMS = [("campaign_info", CampaignInfoForm),
         ("user_conditionals", UserConditionalsForm),
         ("rewards", RewardForm)]

TEMPLATES = {"campaign_info": "campaigns/campaign_info.html",
             "user_conditionals": "campaigns/campaign_info.html",
             "rewards": "campaigns/campaign_info.html"}

class CreateCampaign(SessionWizardView):
    def get_template_names(self):
        return TEMPLATES[self.steps.current]
    form_list = [CampaignInfoForm, UserConditionalsForm, RewardForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    def done(self, form_list, **kwargs):
        for form in form_list:
            print(form.cleaned_data)
        return redirect('/')

class CampaignFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        return redirect('/')



def home(request):
    return render(request, "campaigns/index.html")

def campaigns(request):
    campaigns = serializers.serialize("json", Campaign.objects.all())
    return HttpResponse(campaigns)

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

