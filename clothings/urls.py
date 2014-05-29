# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateClothingView, UpdateClothingView, ClothingListView
)


urlpatterns = patterns(
    '',
    url(r'^list/$', ClothingListView.as_view(), name='list'),
    url(r'^create/$', CreateClothingView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/update/$', UpdateClothingView.as_view(), name='update'),
)
