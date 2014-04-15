# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """
    Portal index page
    """
    template_name = 'portals/index.html'
