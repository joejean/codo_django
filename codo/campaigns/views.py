import os
from django.conf import settings
from django.core import serializers 
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse 
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from formtools.preview import FormPreview
from formtools.wizard.views import SessionWizardView, NamedUrlSessionWizardView
from payments.forms import DirectDonationForm
from payments.payment_utils import create_wepay_merchant, create_wepay_account, wepay_checkout
from payments.models import Merchant, Account
from challenges.utils import get_user_challenges_info, campaign_stats
from .models import Campaign, Organizer, Reward
from .forms import CampaignInfoForm, UserConditionalsForm, RewardFormSet,\
                    OrganizerInfoForm
from .utils import get_organizer, wepay_returns_error, process_wepay_error
from .utils import (show_reward_form, show_conditionals_form,
                    show_organizer_info_form)


FORMS = [("campaign_info", CampaignInfoForm),
         ("user_conditionals", UserConditionalsForm),
         ("rewards", RewardFormSet),
         ("organizer_info", OrganizerInfoForm)]


TEMPLATES = {"campaign_info": "campaigns/campaign_info.html",
             "user_conditionals": "campaigns/user_conditionals.html",
             "rewards": "campaigns/rewards.html",
             "organizer_info": "campaigns/organizer_info.html"}



class CreateCampaign(NamedUrlSessionWizardView):
    condition_dict={
            'rewards':show_reward_form,
            'user_conditionals':show_conditionals_form,
            'organizer_info': lambda w:(show_organizer_info_form(w.request.user)),
            }
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    def done(self,form_list, form_dict,**kwargs):
        account_info = form_dict.get('organizer_info',[])
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
            return redirect('https://stage.wepay.com/v2/oauth2/authorize?client_id=196430&redirect_uri=http://localhost:8000/campaigns/wepay&scope=manage_accounts,collect_payments,view_user,send_money,preapprove_payments,manage_subscriptions')

        return redirect(reverse('single_campaign', kwargs={'pk':campaign.id}))


# TODO: See if I can preview the above form before saving it
class CampaignFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        return redirect('/')


class CampaignsList(ListView):
    model = Campaign
    # This is not mandatory as long as the template name follows the
    # pattern <model_name>_list.html
    template_name = 'campaigns/campaign_list.html'
    context_object_name = 'campaigns'

class CampaignDetail(DetailView):
    model = Campaign
    template_name = 'campaigns/campaign_detail.html'

    def get_context_data(self, **kwargs):
        #Get context dictionary so we can add more stuff to it
        context = super(CampaignDetail, self).get_context_data(**kwargs)
        campaign_id = int(self.kwargs['pk'])
        self.request.session['campaign_id'] = campaign_id
        hasDon, donCon, donAmt, impact = get_user_challenges_info(self.request.user, campaign_id)
        djangoData = {}
        djangoData["user_email"] = str(self.request.user.username)
        djangoData["has_donation"] = str(hasDon).lower()
        djangoData["donation_amt"] = float(donAmt)
        djangoData["impact"] = float(impact)
        djangoData["donation_condition"] = str(donCon)
        djangoData['campaign'] = campaign_id
        djangoData['baseUrl'] = self.request.build_absolute_uri('/')[:-1]
        djangoData['payment_url'] = str(reverse('payment'))
        context['djangoData'] = djangoData
        return context

class ProfileDetail(DetailView):
    model = Organizer
    template_name = 'campaigns/profile_detail.html'

class ProfileUpdate(UpdateView):
    model = Organizer
    form_class = OrganizerInfoForm
    template_name = 'campaigns/profile_update.html'
    #Only let organizers(users) update their own profile
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        #Redirect organizer(user) to their own profile if they try to access
        #another organizer's profile
        if not self.user_passes_test(request):
            return redirect(reverse('profile_update',kwargs={'pk':request.user.id}))
        return super(ProfileUpdate, self).dispatch(
            request, *args, **kwargs)



def index(request):
    campaigns = Campaign.objects.filter(status="accepted")
    stats = []
    #TODO: Do this in a nicer way
    for campaign in campaigns:
        result = campaign_stats(campaign.id)
        stat = {}
        stat['amount_funded'] = result[0] 
        stat['num_funders'] = result[1]
        stat['num_challenges'] =  result[2]
        stats.append(stat)
    campaigns_and_stats = zip(campaigns, stats)
    return render(request, "campaigns/index.html", {'campaigns':campaigns_and_stats}) 

def wepay_success(request):
    code = request.GET.get('code', "")
    response = create_wepay_merchant(code)
    new_merchant = Merchant()
    new_merchant.user = request.user
    new_merchant.access_token = response.get('access_token',"")
    new_merchant.save()
    account = create_wepay_account(new_merchant.access_token)
    new_account = Account()
    new_account.user = request.user
    new_account.account_id = account.get('account_id',"")
    new_account.account_uri = account.get('account_uri',"")
    new_account.save()
    return redirect("/")

def direct_donation(request):
    if request.session.get('campaign_id',""):
        campaign_id = request.session['campaign_id']
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        access_token = campaign.organizer.get_wepay_access_token()
        account_id = campaign.organizer.get_wepay_account_id()
    else:
        return Http404("Campaign does not exist")
    if request.method == 'GET':
        direct_donation_form = DirectDonationForm()
        return render(request, 'payments/direct_donation.html',\
         {'campaign_title':campaign.title,'form':direct_donation_form})
    if request.method == 'POST':
        amount = request.POST.get('amount', "")
        response = wepay_checkout(access_token, account_id, amount, campaign.title)
        if wepay_returns_error(response):
            return process_wepay_error(request, response)
        else:
            response = response.get('hosted_checkout')
            return render(request, 'payments/direct_donation.html',\
            {'checkout_uri':response.get('checkout_uri')} )

def handle_donation(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', "")
        campaign_id = request.POST.get('campaign')
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        access_token = campaign.organizer.get_wepay_access_token()
        account_id = campaign.organizer.get_wepay_account_id()
        response = wepay_checkout(access_token, account_id, amount, campaign.title)
        if wepay_returns_error(response):
            return process_wepay_error(request, response)
        else:
            response = response.get('hosted_checkout')
            return render(request, 'payments/direct_donation.html',\
            {'checkout_uri':response.get('checkout_uri')} )



    
def error(request):
    return render(request, 'campaigns/error.html')





