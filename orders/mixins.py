# -*- coding: utf-8 -*-
from django.http.response import HttpResponseForbidden

from .models import Order


class OrderPermissionMixin(object):
    """
    Permission mixin for Order
    """
    required_roles = ['staff', 'owner']

    def dispatch(self, request, *args, **kwargs):
        """
        Override. Only the designers and the client can see the design
        """
        order = Order.objects.get(code=kwargs['code'])
        if 'owner' in self.required_roles and self.request.user == order.creator:
            return super(OrderPermissionMixin, self).dispatch(request, *args, **kwargs)  # noqa

        if 'staff' in self.required_roles and self.request.user.is_staff:
            return super(OrderPermissionMixin, self).dispatch(request, *args, **kwargs)  # noqa

        return HttpResponseForbidden()
