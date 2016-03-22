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
from payments.forms import DirectDonationForm
from payments.payment_utils import create_wepay_merchant, create_wepay_account, wepay_checkout
from payments.models import Merchant, Account

FORMS = [("campaign_info", CampaignInfoForm),
         ("user_conditionals", UserConditionalsForm),
         ("rewards", RewardFormSet),
         ("account_info", AccountInfoForm)]


TEMPLATES = {"campaign_info": "campaigns/campaign_info.html",
             "user_conditionals": "campaigns/user_conditionals.html",
             "rewards": "campaigns/rewards.html",
             "account_info": "campaigns/account_info.html"}

#Create Campaign Helper function
def get_organizer(user, account_info):
    organizer = Organizer.objects.filter(user=user)
    if len(organizer) == 0:
        new_organizer = account_info.save(commit=False)
        new_organizer.user = user
        new_organizer.save()
    else:
        new_organizer = organizer[0]

    return new_organizer

class CreateCampaign(NamedUrlSessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    def done(self,form_list, form_dict,**kwargs):
        account_info = form_dict['account_info']
        campaign_info = form_dict['campaign_info']
        user_conditionals = form_dict.get('user_conditionals', [])
        rewards = form_dict.get('rewards', [])

        organizer = get_organizer(self.request.user, account_info)
        campaign = campaign_info.save(commit=False)
        campaign.organizer = organizer

        if user_conditionals:
            conditionals = user_conditionals.cleaned_data
            campaign.friends_participation_cond = conditionals['friends_participation_cond']
            campaign.friends_participation_amount_cond = conditionals['friends_participation_amount_cond']
            campaign.community_participation_cond = conditionals['community_participation_cond']
            campaign.community_participation_amount_cond = conditionals['community_participation_amount_cond']
            campaign.milestone_cond = conditionals['milestone_cond']
            campaign.matching_donation_cond = conditionals['matching_donation_cond']
        campaign.save()

        if rewards:
            new_rewards = rewards.save(commit=False)
            for reward in new_rewards:
                reward.campaign = campaign
                reward.save()
        merchant = Merchant.objects.filter(user=self.request.user)
        if not merchant:
            return redirect('https://stage.wepay.com/v2/oauth2/authorize?client_id=196430&redirect_uri=http://localhost:8000/wepay&scope=manage_accounts,collect_payments,view_user,send_money,preapprove_payments,manage_subscriptions')

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
        request.session['campaign_id'] = campaign.id
        request.session['campaign_title'] = campaign.title
        request.session['account_id'] = campaign.organizer.get_wepay_account_id() 
        request.session['access_token'] = campaign.organizer.get_wepay_access_token()
        rewards = campaign.reward_set.all()
        return render(request,"campaigns/campaign_page.html",\
         {'campaign':campaign, 'rewards': rewards})


def wepay_success(request):
    code = request.GET.get('code', "")
    response = create_wepay_merchant(code)
    print('CREATE MERCHANT')
    print(response)
    new_merchant = Merchant()
    new_merchant.user = request.user
    new_merchant.access_token = response.get('access_token',"")
    new_merchant.save()
    account = create_wepay_account(new_merchant.access_token)
    print('PRINTING ACCOUNT')
    print(account)
    new_account = Account()
    new_account.user = request.user
    new_account.account_id = account.get('account_id',"")
    new_account.account_uri = account.get('account_uri',"")
    new_account.save()
    return redirect("/")

def direct_donation(request):
    if request.session.get('campaign_id',""):
        campaign_id = request.session['campaign_id']
    if request.session.get('campaign_title'):
        campaign_title = request.session['campaign_title']
    if request.session.get('access_token'):
        access_token = request.session['access_token']
    if request.session.get('account_id'):
        account_id = request.session['account_id']

    if request.method == 'GET':
        direct_donation_form = DirectDonationForm()
        return render(request, 'payments/direct_donation.html',\
         {'campaign_title':campaign_title,'form':direct_donation_form})
    if request.method == 'POST':
        amount = request.POST.get('amount', "")
        response = wepay_checkout(access_token, account_id, amount, campaign_title)
        response = response.get('hosted_checkout')
        print(response)
        return render(request, 'payments/direct_donation.html',\
        {'checkout_uri':response.get('checkout_uri')} )

    






