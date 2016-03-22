from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from . import views

campaign_wizard = login_required(views.CreateCampaign.as_view(views.FORMS,
                  url_name='campaign_step',
                  done_step_name='finished',
                  condition_dict={'rewards':views.show_reward_form,
                  'user_conditionals':views.show_conditionals_form}), 
                  login_url='/accounts/login',
                  )


urlpatterns = patterns('',
                       url(r'^$', views.home),
                       url(r'^new_campaign/(?P<step>.+)/$', campaign_wizard, name='campaign_step'),
                       url(r'^new_campaign/$', campaign_wizard, name='new_campaign'),
                       url(r'^all_campaigns/$', views.campaigns, name='campaigns_list'),
                       url(r'^campaign/(?P<id>[0-9]+)$', views.campaigns, name='single_campaign'),
                       url(r'^wepay/$', views.wepay_success, name="wepay_redirect"),
                       url(r'^direct_donation/$', views.direct_donation, name="direct_donation"),
                       )