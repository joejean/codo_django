"""
This module contains all the functions that help handle payment.
Our payment system is built on top of Stripe. Stripe requires that
all requests be made over HTTPS.
"""
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_account(email, first_name, last_name, dob, ip, timestamp,
                          country="US"):
    """creates a new Stripe (managed) account for a campaign organizer.
    :param country: the country the account holder resides in. Optional.
    :returns: Stripe account ID
    """
    account = stripe.Account.create(
        managed=True,
        country=country,
        email=email,
        legal_entity={'first_name': first_name,
                      'last_name': last_name,
                      'dob': {'day': dob.get('day'),
                              'month': dob.get('month'),
                              'year': dob.get('year')
                              },
                      'type': 'individual'
                      },
        tos_acceptance={'ip': ip,
                        'date': timestamp
                        }
    )
    return account.id


def create_bank_account(accnt_id, account_number, country, currency,
                        routing_number="110000000"):
    """Creates a Stripe bank account object
    :param accnt_id: Stripe Account For Which you are creating the bank account
    :param account_number: The account number for the bank account in string form. Must
                           be a checking account.
    :param routing_number: The routing number, sort code, or other country-appropriate
                           institution number for the bank account. For US bank
                           accounts,this is required and should be the ACH routing 
                           number, not the wire routing number. If you are providing
                           an IBAN for account_number, this field is not required.
    :returns: Stripe bank account object
    """
    account = stripe.Account.retrieve(accnt_id)
    bank_account = account.external_accounts.create(
        external_account={'object': 'bank_account',
                           'country': country,
                           'currency': currency,
                           'account_number': account_number,
                           'routing_number': routing_number
                           })

    return bank_account


def charge_account(amnt, source, destination, currency='usd'):
    """charges an account for the specified amount.

    """
    stripe.Charge.create(
        amount=amnt,
        currency=currency,
        source=source,
        destination=destination
    )
