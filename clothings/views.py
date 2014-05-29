# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import SuperuserRequiredMixin

from .models import Clothing


class CreateClothingView(SuperuserRequiredMixin, CreateView):
    """
    View for create new clothing
    """
    model = Clothing
    success_url = reverse_lazy('clothings:list')


class UpdateClothingView(SuperuserRequiredMixin, UpdateView):
    """
    View for update clothing object
    """
    model = Clothing
    success_url = reverse_lazy('clothings:list')


class ClothingListView(SuperuserRequiredMixin, ListView):
    """
    Display all the clothings
    """
    model = Clothing

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(ClothingListView, self).get_context_data(**kwargs)
        data.update({'clothing_choices': Clothing.CATEGORY_CHOICES})
        data.update(self.request.GET.dict())
        return data

    def get_queryset(self):
        """
        Filter clothings
        """
        qs = super(ClothingListView, self).get_queryset()

        # category
        category = self.request.REQUEST.get('category', 'all')
        if category == 'all':
            category_Q = Q()
        else:
            category_Q = Q(category=category)

        return qs.filter(category_Q)
