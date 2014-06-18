# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    LoginView, LogoutView, RegisterView, UploadView, UpdateProfileView,
    CreateRandomUserView, PhoneLoginView, SendTemporaryPasswordView
)


urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^phone_login/$', PhoneLoginView.as_view(), name='phone_login'),
    url(r'^send_temporary_password/$',
        SendTemporaryPasswordView.as_view(), name='send_temporary_password'),
    url(r'^create_random_user/$', CreateRandomUserView.as_view(),
        name='create_random_user'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^update/$', UpdateProfileView.as_view(), name='update'),
)
