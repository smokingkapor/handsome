# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateClothingView, UpdateClothingView, ClothingListView,
    ClothingSearchView, SupplierListView, CreateSupplierView,
    UpdateSupplierView
)


urlpatterns = patterns(
    '',
    url(r'^list/$', ClothingListView.as_view(), name='list'),
    url(r'^search/$', ClothingSearchView.as_view(), name='search'),
    url(r'^create/$', CreateClothingView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/update/$', UpdateClothingView.as_view(), name='update'),
    url(r'^supplier/list/$', SupplierListView.as_view(), name='supplier_list'),
    url(r'^supplier/create/$',
        CreateSupplierView.as_view(), name='create_supplier'),
    url(r'^supplier/(?P<pk>\d+)/update/$',
        UpdateSupplierView.as_view(), name='update_supplier'),
)
