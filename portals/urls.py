# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import IndexView, SurveyView, SurveyPriceView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^survey/$', SurveyView.as_view(), name='survey'),
    url(r'^survey/price/$', SurveyPriceView.as_view(), name='survey_price'),
)
