# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import CreateOrderView


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateOrderView.as_view(), name='create'),
)
