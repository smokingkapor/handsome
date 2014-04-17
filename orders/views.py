# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin, AjaxResponseMixin

from .forms import CreateOrderForm
from .models import Order
from braces.views._ajax import JSONResponseMixin


class CreateOrderView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
                      CreateView):
    """
    Create order 
    """
    model = Order
    form_class = CreateOrderForm

    def form_valid(self, form):
        """
        Override. Set current user as creator. Return JSON if it's AJAX.
        """
        order = form.save(commit=False)
        order.creator = self.request.user
        order.save()

        if self.request.is_ajax():
            return self.render_json_response({'success': True})

        return super(CreateOrderView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Override. Return JSON if it's AJAX.
        """
        if self.request.is_ajax():
            return self.render_json_response({'success': False})
        return super(CreateOrderView, self).form_invalid(form)
