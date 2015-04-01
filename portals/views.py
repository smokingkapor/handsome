# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin

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
            'onekeymode': self.request.GET.get('mode') == 'onekey',
            'SITUATION_CHOICES': Order.SITUATION_CHOICES,
            'USUAL_DRESS_OPTIONS': Profile.USUAL_DRESS_OPTIONS,
            'PREFERRED_DRESS_OPTIONS': Profile.PREFERRED_DRESS_OPTIONS
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
            'CLOTHING_SIZE_CHOICES': Profile.CLOTHING_SIZE_CHOICES,
            'PANTS_SIZE_CHOICES': Profile.PANTS_SIZE_CHOICES,
            'PANTS_STYLE_CHOICES': Profile.PANTS_STYLE_CHOICES
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


class RobotsView(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(mimetype='text/plain')
        response.write('User-agent: *\nDisallow:\nAllow: /')
        return response
