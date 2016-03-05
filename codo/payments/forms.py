from django import forms

class DirectDonationForm(forms.Form):
    amount = forms.DecimalField(max_digits=15, decimal_places=2)