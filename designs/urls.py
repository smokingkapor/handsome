# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateDesignView, UploadView, DesignDetailView, AcceptDesignView,
    RejectDesignView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateDesignView.as_view(), name='create'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^(?P<pk>\d+)/$', DesignDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/select/$', AcceptDesignView.as_view(), name='accept'),
    url(r'^(?P<pk>\d+)/select/$', RejectDesignView.as_view(), name='reject'),
)
