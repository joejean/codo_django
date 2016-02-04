from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class ProjectForm(forms.Form):
    title = forms.CharField()
    blurb = forms.CharField()
    category = forms.ChoiceField(choices=[('Art','Art'), ('Education', 'Education')])
    description = forms.CharField(widget="textarea")
    image = forms.CharField()
    video_url = forms.CharField()
    funding_goal = forms.IntegerField(min_value='100')
    funding_period = forms.IntegerField(min_value='1')


