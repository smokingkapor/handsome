# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    LoginView, LogoutView, RegisterView, UploadView, UpdateProfileView
)


urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^update/$', UpdateProfileView.as_view(), name='update'),
)
