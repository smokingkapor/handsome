# -*- coding: utf-8 -*-
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, StaffuserRequiredMixin, AjaxResponseMixin,
    JSONResponseMixin, LoginRequiredMixin
)

from .models import Clothing, Supplier


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
        data.update({'clothing_choices': Clothing.CATEGORY_CHOICES,
                     'suppliers': Supplier.objects.all()})
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

        # supplier
        supplier = self.request.REQUEST.get('supplier', 'all')
        if supplier == 'all':
            supplier_Q = Q()
        else:
            supplier_Q = Q(supplier__id=supplier)

        return qs.filter(category_Q, supplier_Q)


class ClothingSearchView(StaffuserRequiredMixin, AjaxResponseMixin,
                         JSONResponseMixin, View):
    """
    Search clothing
    """
    page_size = 20

    def search(self, category, name, page):
        """
        Search clothings
        """
        category_Q = Q()
        if category:
            category_Q = Q(category=category)

        name_Q = Q()
        if name:
            name_Q = Q(name__contains=name)

        start = page*self.page_size
        end = start + self.page_size
        return Clothing.objects.filter(category_Q, name_Q).filter(is_active=True)[start:end]  # noqa

    def get_ajax(self, request, *args, **kwargs):
        """
        Do ajax search
        """
        category = request.REQUEST.get('category')
        if not category or category == 'all':
            category = None
        name = request.REQUEST.get('name')
        if not name:
            name = None
        page = request.REQUEST.get('page')
        if not page:
            page = 0
        else:
            page = int(page)

        clothings = []
        for clo in self.search(category, name, page):
            clothings.append({
                'pk': clo.id,
                'name': clo.name,
                'sku': clo.sku,
                'price': clo.price,
                'sizes': clo.sizes,
                'colors': clo.colors,
                'note': clo.note,
                'image': clo.medium_image,
                'is_active': clo.is_active,
                'category': clo.category
            })
        return self.render_json_response(clothings)


class SupplierListView(SuperuserRequiredMixin, ListView):
    """
    Display all suppliers
    """
    model = Supplier


class CreateSupplierView(SuperuserRequiredMixin, CreateView):
    """
    Create new supplier
    """
    model = Supplier
    success_url = reverse_lazy('clothings:supplier_list')


class UpdateSupplierView(SuperuserRequiredMixin, UpdateView):
    """
    Update supplier info
    """
    model = Supplier
    success_url = reverse_lazy('clothings:supplier_list')


class ClothingPhotosView(LoginRequiredMixin, DetailView):
    model = Clothing
    template_name = 'clothings/clothing_photos.html'
