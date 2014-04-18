# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from braces.views import(
    LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin
)

from .forms import CreateOrderForm
from .models import Order, Province, City, Country


class CreateOrderView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
                      CreateView):
    """
    Create order 
    """
    model = Order
    form_class = CreateOrderForm
    template_name = 'orders/create_order.html'

    def get_context_data(self, **kwargs):
        """
        Override. Add extra data to context
        """
        data = super(CreateOrderView, self).get_context_data(**kwargs)
        data.update({'provinces': Province.objects.all()})
        return data

    def form_valid(self, form):
        """
        Override. Set current user as creator. Return JSON if it's AJAX.
        """
        profile = self.request.user.profile

        order = form.save(commit=False)
        order.prepayment = order.total_price * 0.1
        order.creator = profile.user
        order.style = profile.preferred_style
        order.age_group = profile.age_group
        order.height = profile.height
        order.weight = profile.weight
        order.waistline = profile.waistline
        order.chest = profile.chest
        order.hipline = profile.hipline
        order.foot = profile.foot
        order.preferred_designer = profile.user
        order.save()

        if self.request.is_ajax():
            url = reverse('orders:create_success', kwargs={'pk': order.id})
            return self.render_json_response({'success': True, 'next': url})

        return super(CreateOrderView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Override. Return JSON if it's AJAX.
        """
        if self.request.is_ajax():
            return self.render_json_response({'success': False})
        return super(CreateOrderView, self).form_invalid(form)


class LoadAddressView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
                      View):
    """
    Load cities or countries or towns.
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Load address data.
        """
        level = request.GET['level']
        pk = request.GET['pk']
        if level == 'city':
            objs = Province.objects.get(pk=pk).city_set.all()
            return self.render_json_object_response(objs)
        elif level == 'country':
            objs = City.objects.get(pk=pk).country_set.all()
            return self.render_json_object_response(objs)
        elif level == 'town':
            objs = Country.objects.get(pk=pk).town_set.all()
            return self.render_json_object_response(objs)


class CreateSuccessView(LoginRequiredMixin, DetailView):
    """
    Order create success page view
    """
    model = Order
    template_name = 'orders/create_order_success.html'


class MyOrderView(LoginRequiredMixin, ListView):
    """
    Display all my orders
    """
    model = Order
    template_name = 'orders/me.html'

    def get_queryset(self):
        """
        My orders only
        """
        qs = super(MyOrderView, self).get_queryset()
        return qs.filter(creator=self.request.user).order_by('-created_at')
