# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateOrderView, LoadAddressView, CreateSuccessView, MyOrderView,
    OrderListView, PrepayView, PayView, SendView, ReceiveView, OrderDetailView,
    OrderClothingsView, SaveAddressView, RefundView, FinishDesignView,
    OrderSupplierClothingsView, SelectClothingView, UpdateAddressView,
    ReturnView, ReceiveReturnView, RedesignView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateOrderView.as_view(), name='create'),
    url(r'^clothings/$', OrderClothingsView.as_view(), name='clothings'),
    url(r'^supplier_clothings/$',
        OrderSupplierClothingsView.as_view(), name='supplier_clothings'),
    url(r'^me/$', MyOrderView.as_view(), name='me'),
    url(r'^load_address/$', LoadAddressView.as_view(), name='load_address'),
    url(r'^save_address/$', SaveAddressView.as_view(), name='save_address'),
    url(r'^update_address/$', UpdateAddressView.as_view(), name='update_address'),
    url(r'^(?P<code>\d+)/create_success/$', CreateSuccessView.as_view(),
        name='create_success'),
    url(r'^(?P<code>\d+)/$', OrderDetailView.as_view(), name='detail'),
    url(r'^list/$', OrderListView.as_view(), name='list'),
    url(r'^(?P<code>\d+)/finish_design/$',
        FinishDesignView.as_view(), name='finish_design'),
    url(r'^(?P<code>\d+)/prepay/$', PrepayView.as_view(), name='prepay'),
    url(r'^(?P<code>\d+)/pay/$', PayView.as_view(), name='pay'),
    url(r'^(?P<code>\d+)/send/$', SendView.as_view(), name='send'),
    url(r'^(?P<code>\d+)/receive/$', ReceiveView.as_view(), name='receive'),
    url(r'^(?P<code>\d+)/refund/$', RefundView.as_view(), name='refund'),
    url(r'^return/$', ReturnView.as_view(), name='return'),
    url(r'^(?P<code>\d+)/receive_return/$', ReceiveReturnView.as_view(), name='receive_return'),
    url(r'^(?P<code>\d+)/select_clothing/$', SelectClothingView.as_view(), name='select_clothings'),
    url(r'^(?P<code>\d+)/redesign/$', RedesignView.as_view(), name='redesign'),
)
