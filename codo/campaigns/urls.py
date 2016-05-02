from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from . import views
from .utils import (show_reward_form, show_conditionals_form,
                    show_organizer_info_form)
                    
campaign_wizard = login_required(views.CreateCampaign.as_view(views.FORMS,
                  url_name='campaign_step',
                  done_step_name='finished'), 
                  login_url='/accounts/login',
                  )


urlpatterns = \
patterns('',
         url(r'^$', views.index),
         url(r'^new_campaign/(?P<step>.+)/$', campaign_wizard, name='campaign_step'),
         url(r'^new_campaign/$', campaign_wizard, name='new_campaign'),
         url(r'^campaigns/$', views.CampaignsList.as_view(), name='campaigns_list'),
         url(r'^campaigns/(?P<pk>[0-9]+)$', views.CampaignDetail.as_view(), name='single_campaign'),
         url(r'^wepay/$', views.wepay_success, name="wepay_redirect"),
         url(r'^direct_donation/$', views.direct_donation, name="direct_donation"),
         url(r'^error/$', views.error, name="campaign_error"),
         url(r'^profile/(?P<pk>[0-9]+)/update/$', login_required(views.ProfileUpdate.as_view()),\
              name="profile_update"),
         url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view(),\
              name="profile_detail"),
         url(r'^search/', include('haystack.urls')),
        )