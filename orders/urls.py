# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateOrderView, LoadAddressView, CreateSuccessView, MyOrderView,
    OrderListView, PrepayView, PayView, SendView, ReceiveView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateOrderView.as_view(), name='create'),
    url(r'^me/$', MyOrderView.as_view(), name='me'),
    url(r'^load_address/$', LoadAddressView.as_view(), name='load_address'),
    url(r'^(?P<code>\d+)/create_success/$', CreateSuccessView.as_view(),
        name='create_success'),
    url(r'^list/$', OrderListView.as_view(), name='list'),
    url(r'^(?P<code>\d+)/prepay/$', PrepayView.as_view(), name='prepay'),
    url(r'^(?P<code>\d+)/pay/$', PayView.as_view(), name='pay'),
    url(r'^(?P<code>\d+)/send/$', SendView.as_view(), name='send'),
    url(r'^(?P<code>\d+)/receive/$', ReceiveView.as_view(), name='receive'),
)
