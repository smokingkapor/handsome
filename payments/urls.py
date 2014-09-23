# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    PayView, SuccessView, NotifyView, HomeView, RefundView, RefundNotifyView
)


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^pay/$', PayView.as_view(), name='pay'),
    url(r'^success/$', SuccessView.as_view(), name='success'),
    url(r'^notify/$', NotifyView.as_view(), name='notify'),
    url(r'^refund/$', RefundView.as_view(), name='refund'),
    url(r'^refund_notify/$', RefundNotifyView.as_view(), name='refund_notify'),
)
