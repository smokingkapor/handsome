# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView

from accounts.models import Profile


class IndexView(TemplateView):
    """
    Portal index page
    """
    template_name = 'portals/index.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(IndexView, self).get_context_data(**kwargs)
        data.update({'STYLE_CHOICES': Profile.STYLE_CHOICES,
                     'AGE_GROUP_CHOICES': Profile.AGE_GROUP_CHOICES})
        return data