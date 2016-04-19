from .models import Campaign, Organizer, Reward
from django.shortcuts import redirect
from django.contrib import messages
from django.core.urlresolvers import reverse 

#Returns an organizer if one already exists
#if not, Create one from the account_info object parameter, 
#update it and save it to the DB.
def get_organizer(user, account_info):
    # If account info is not an empty list, we need to update the organizer's
    # Account if they exist in the db or just create a new one
    if account_info: 
        try:
            organizer = Organizer.objects.get(user=user)
            if not organizer.phone_number:
                organizer.phone_number = account_info.cleaned_data['phone_number']
                organizer.short_bio = account_info.cleaned_data['short_bio']
                organizer.profile_picture = account_info.cleaned_data['profile_picture'] #this is my file field
                organizer.facebook_url = account_info.cleaned_data['facebook_url']
                organizer.twitter_url = account_info.cleaned_data['twitter_url']
                organizer.website_url = account_info.cleaned_data['website_url']
                organizer.dob = account_info.cleaned_data['dob']
                organizer.save()
            new_organizer = organizer
        except Organizer.DoesNotExist:
            new_organizer = account_info.save(commit=False)
            new_organizer.user = user
            new_organizer.save()
    else:
        new_organizer = Organizer.objects.get(user=user)

    return new_organizer


def wepay_returns_error(response):
    if response.get("error", None) is not None:
        return True
    return False

def process_wepay_error(request, wepay_response):
    if wepay_response.get("error_code", None) == 1011:
        #1011: The access_token you passed has been revoked
        #TODO: notify_campaign_organizer to regive us authorization (via) wepay
        #redirect user to (error) Page to explain and apologize
        messages.error(request,\
         'We are sorry. We were unable to process the payment for this particular campaign.')
        return redirect(reverse('campaign_error'))

    #TODO: Implement more error checking/processing

# Return true if user selected 'rewards_enabled' in previous step
# false otherwise
def show_reward_form(wizard):
    # try to get the cleaned data of step 1
    cleaned_data = wizard.get_cleaned_data_for_step('campaign_info') or {}
    # check if the field ``enable reward`` was checked.
    return cleaned_data.get('rewards_enabled', True)

# Return true if user selected 'conditionals_enabled' in previous step
# false otherwise
def show_conditionals_form(wizard):
    # try to get the cleaned data of step 1
    cleaned_data = wizard.get_cleaned_data_for_step('campaign_info') or {}
    # check if the field ``enable reward`` was checked.
    return cleaned_data.get('conditionals_enabled', True)

def show_organizer_info_form(user):
    organizer = Organizer.objects.filter(user=user)
    return organizer[0].phone_number == ''

