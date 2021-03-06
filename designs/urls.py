# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateDesignView, UploadView, DesignDetailView, AcceptDesignView,
    RemoveDesignView, DesignPhotosView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateDesignView.as_view(), name='create'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^(?P<code>\d+)/$', DesignDetailView.as_view(), name='detail'),
    url(r'^(?P<code>\d+)/remove/$', RemoveDesignView.as_view(), name='remove'),
    url(r'^(?P<code>\d+)/select/$', AcceptDesignView.as_view(), name='accept'),
    url(r'^(?P<code>\d+)/photos/$', DesignPhotosView.as_view(), name='photos'),
    # url(r'^(?P<code>\d+)/reject/$', RejectDesignView.as_view(), name='reject'),
)
