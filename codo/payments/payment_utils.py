# WePay Python SDK - http://git.io/v7Y1jA
from wepay import WePay
from django.conf import settings

def create_wepay_merchant(code):
    redirect_uri = settings.WEPAY_REDIRECT_URI
    client_id = settings.WEPAY_CLIENT_ID
    client_secret = settings.WEPAY_CLIENT_SECRET
    production = settings.WEPAY_PRODUCTION
    # set production to True for live environments
    wepay = WePay(production, None)
    # Get a Token to later create an account for a user
    try:
        response = wepay.get_token(redirect_uri, client_id, client_secret, code)
    except:
        response = "Error"
    
    return response

def create_wepay_account(access_token):
    # set production to True for live environments
    production = settings.WEPAY_PRODUCTION
    # Use access token to create account for a user.
    wepay = WePay(production, access_token)
    response = wepay.call('/account/create', {
    'name': 'Codo Project Contribution',
    'description': 'Crowdfunding Platform'
    })
    return response


def wepay_checkout(access_token, account_id, amount, campaign_title):
    redirect_uri = settings.WEPAY_DONATION_SUCCESS_REDIRECT_URI
    # set production to True for live environments
    production = settings.WEPAY_PRODUCTION
    wepay = WePay(production, access_token)
    parameters = {
    'account_id': account_id,
    'amount': amount,
    'short_description': 'Contribution to Codo\'s {}'.format(campaign_title),
    'type': 'donation',
    'currency': 'USD',
    'hosted_checkout':  {
        "mode": "iframe"
        },
    }
    if redirect_uri is not None:
        parameters['callback_uri'] = redirect_uri
    response = wepay.call('/checkout/create', parameters)
    return response

