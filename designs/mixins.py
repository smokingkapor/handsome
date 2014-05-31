# -*- coding: utf-8 -*-
from django.http.response import HttpResponseForbidden

from .models import Design


class DesignPermissionMixin(object):
    """
    Permission mixin for design
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Override. Only the designers and the client can see the design
        """
        design = Design.objects.get(pk=kwargs['pk'])
        if not self.request.user.is_staff and self.request.user != design.client:
            return HttpResponseForbidden()
        return super(DesignPermissionMixin, self).dispatch(request, *args, **kwargs)
