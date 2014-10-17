# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    PromoListView, CreatePromoView, UpdatePromoView, VerifyPromoView
)


urlpatterns = patterns(
    '',
    url(r'^list/$', PromoListView.as_view(), name='list'),
    url(r'^create/$', CreatePromoView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/update/$', UpdatePromoView.as_view(), name='update'),
    url(r'^verify/$', VerifyPromoView.as_view(), name='verify'),
)
