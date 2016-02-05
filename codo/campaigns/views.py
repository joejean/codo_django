from django.core import serializers 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Campaign


def home(request):
    return render(request, "campaigns/index.html")

def campaigns(request):
    campaigns = serializers.serialize("json", Campaign.objects.all())
    return HttpResponse(campaigns)

def all_projects(request):
    return render(request, "campaigns/all-projects.html")

@login_required(login_url='/login')
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
    return render(request, 'campaigns/create-campaign.html')

# Login, Logout, Signup
def login_view(request):
    next = ''
    if request.GET:
        next = request.GET['next']

    if request.method == 'POST':
        if 'username' in request.POST:
            username = request.POST['username']
        if 'password' in request.POST:
            password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # TODO: redirect to a success page
                return redirect(next) if next else HttpResponse("You are now logged in %s" % user.username)
            else:
                # TODO: Proper error message for inactive account
                return HttpResponse("This account is disabled")
        else:
            # TODO: Proper error message for invalid login
            return HttpResponse("Invalid login")
    return render(request, 'campaigns/login.html')


def logout_view(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == 'POST':
        if 'first_name' in request.POST:
            first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            last_name = request.POST['last_name']
        if 'username' in request.POST:
            username = request.POST['username']
        if 'email' in request.POST:
            email = request.POST['email']
        if 'password' in request.POST:
            password = request.POST['password']
        User.objects.create_user(username=username, email=email,
                                 password=password, first_name=first_name,
                                 last_name=last_name)
        # TODO: Error Checking in case the user existed already
        return redirect("/login")
    else:
        return render(request, 'campaigns/signup.html')