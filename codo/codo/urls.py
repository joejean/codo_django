from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'codo.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.home),
                       url(r'^login/$', views.login_view),
                       url(r'^logout/$', views.logout_view),
                       url(r'^signup/$', views.signup),
                       url(r'^new_campaign/$', views.create_campaign),
                       url(r'^campaigns/$', views.campaigns),
                       url(r'^all_projects/$', views.all_projects),
                       )
