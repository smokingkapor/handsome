# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    LoginView, LogoutView, RegisterView,
    CreateRandomUserView, PhoneLoginView, SendTemporaryPasswordView,
    CreatePhotoView, RemovePhotoView, ProfileView, UpdateProfileView,
    UpdatePasswordView, DesignerCaseView
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
    url(r'^create_photo/$', CreatePhotoView.as_view(), name='create_photo'),
    url(r'^remove_photo/$', RemovePhotoView.as_view(), name='remove_photo'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^update_profile/$', UpdateProfileView.as_view(), name='update_profile'),
    url(r'^update_password/$', UpdatePasswordView.as_view(), name='update_password'),
    url(r'^(?P<pk>\d+)/case/$', DesignerCaseView.as_view(), name='designer_case'),
)
