# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import IndexView, SurveyView, SurveyMoreView, StaticPageView, RobotsView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^survey/$', SurveyView.as_view(), name='survey'),
    url(r'^survey/more/$', SurveyMoreView.as_view(), name='survey_more'),
    url(r'^portals/(?P<template_name>.+)/$', StaticPageView.as_view(), name='static_page'),
    url(r'^robots.txt$', RobotsView.as_view(), name='robots'),
)
