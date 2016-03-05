from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from campaigns import views



campaign_wizard = login_required(views.CreateCampaign.as_view(views.FORMS,
                  url_name='campaign_step',
                  done_step_name='finished',
                  condition_dict={'rewards':views.show_reward_form,
                  'user_conditionals':views.show_conditionals_form}), 
                  login_url='/accounts/login',
                  )

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'codo.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.home),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^new_campaign/(?P<step>.+)/$', campaign_wizard, name='campaign_step'),
                       url(r'^new_campaign/$', campaign_wizard, name='campaign'),
                       url(r'^campaigns/$', views.campaigns),
                       url(r'^campaigns/(?P<id>[0-9]+)$', views.campaigns),
                       url(r'^all_projects/$', views.all_projects),
                       url(r'^wepay/$', views.wepay_success),
                       )
