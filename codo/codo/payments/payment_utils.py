# WePay Python SDK - http://git.io/v7Y1jA
from wepay import WePay
from django.conf import settings


def create_merchant(code):
    redirect_uri = settings.WEPAY_REDIRECT_URI
    client_id = settings.WEPAY_CLIENT_ID
    client_secret = settings.WEPAY_CLIENT_SECRET
    production = settings.WEPAY_PRODUCTION
    # set production to True for live environments
    wepay = WePay(production, None)
    # create an account for a user
    response = wepay.get_token(redirect_uri, client_id, client_secret, code)
    return response

def create_account(access_token):
    # set production to True for live environments
    wepay = WePay(production, access_token)
    response = wepay.call('/account/create', {
    'name': 'Codo Project Contribution',
    'description': 'Crowdfunding Platform'
})
    return response
