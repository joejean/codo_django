from django.conf.urls import patterns, include, url
from django.contrib import admin
from campaigns import views


campaign_wizard = views.CreateCampaign.as_view(views.FORMS,url_name='campaign_step',\
                   done_step_name='finished')

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'codo.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.home),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^new_campaign/(?P<step>.+)/$', campaign_wizard, name='campaign_step'),
                       url(r'^new_campaign/$', campaign_wizard, name='campaign'),
                       #url(r'^create_campaign/$', views.CreateCampaign.as_view(views.FORMS)),#views.FORMS
                       url(r'^campaigns/$', views.campaigns),
                       url(r'^all_projects/$', views.all_projects),
                       )
