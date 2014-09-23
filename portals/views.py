# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin

from accounts.constants import BUSINESS, CASUAL, ENGLAND, CASUAL_BUSINESS
from accounts.forms import ProfileForm
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
        data.update({
            'STYLE_CHOICES': Profile.STYLE_CHOICES,
            'designers': Profile.objects.filter(user__is_staff=True, is_designer=True),
            'STYLE_IMAGES': {
                BUSINESS: range(1, 6),
                CASUAL: range(1, 7),
                ENGLAND: range(1, 6),
                CASUAL_BUSINESS: range(1, 6)
            }
        })
        return data


class SurveyMoreView(LoginRequiredMixin, FormView):
    """
    Survey for price, personal data and more requirements
    """
    template_name = 'portals/survey_more.html'
    form_class = ProfileForm
    success_url = reverse_lazy('orders:create')

    def get_form_kwargs(self):
        """
        Add user profile to the form
        """
        kwargs = super(SurveyMoreView, self).get_form_kwargs()
        kwargs.update({'instance': self.request.user.profile})
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(SurveyMoreView, self).get_context_data(**kwargs)
        data.update({
            'AGE_GROUP_CHOICES': Profile.AGE_GROUP_CHOICES,
            'STYLE_CHOICES': Profile.STYLE_CHOICES,
            'CLOTHING_SIZE_CHOICES': Profile.CLOTHING_SIZE_CHOICES,
            'PANTS_SIZE_CHOICES': Profile.PANTS_SIZE_CHOICES,
            'PANTS_STYLE_CHOICES': Profile.PANTS_STYLE_CHOICES,
            'SHOE_SIZE_CHOICES': Profile.SHOE_SIZE_CHOICES,
            'COLOR_CHOICES': Profile.COLOR_CHOICES,
            'SITUATION_CHOICES': Order.SITUATION_CHOICES,
            'designers': Profile.objects.filter(user__is_staff=True, is_designer=True),  # noqa
        })
        return data

    def form_valid(self, form):
        """
        Save profile data
        """
        form.save()
        return super(SurveyMoreView, self).form_valid(form)


class StaticPageView(TemplateView):

    def get_template_names(self):
        return 'portals/{}.html'.format(self.kwargs['template_name'])
