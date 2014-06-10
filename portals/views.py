# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView

from braces.views import LoginRequiredMixin

from accounts.models import Profile
from orders.models import Order


class IndexView(TemplateView):
    """
    Portal index page
    """
    template_name = 'portals/index.html'


class SurveyView(TemplateView):
    """
    User info survey
    """
    template_name = 'portals/survey.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(SurveyView, self).get_context_data(**kwargs)
        data.update({'STYLE_CHOICES': Profile.STYLE_CHOICES,
                     'AGE_GROUP_CHOICES': Profile.AGE_GROUP_CHOICES,
                     'PRICE_CHOICES': Order.PRICE_CHOICES,
                     'designers': Profile.objects.filter(user__is_staff=True,
                                                         is_designer=True)})
        return data


class SurveyPriceView(LoginRequiredMixin, TemplateView):
    """
    Price select view
    """
    template_name = 'portals/survey_price.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(SurveyPriceView, self).get_context_data(**kwargs)
        data.update({'PRICE_CHOICES': Order.PRICE_CHOICES})
        return data
