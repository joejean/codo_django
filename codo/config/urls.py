from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from campaigns import views


urlpatterns = patterns('',
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^$', views.index, name='index'),
                       url(r'^campaigns/', include('campaigns.urls')),
                       )
