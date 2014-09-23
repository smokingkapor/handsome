# -*- coding: utf-8 -*-
from django.http.response import HttpResponseForbidden

from .models import Design


class DesignPermissionMixin(object):
    """
    Permission mixin for design
    """
    required_roles = ['staff', 'owner']

    def dispatch(self, request, *args, **kwargs):
        """
        Override. Only the designers and the client can see the design
        """
        design = Design.objects.get(code=kwargs['code'])
        if 'owner' in self.required_roles and self.request.user == design.client:
            return super(DesignPermissionMixin, self).dispatch(request, *args, **kwargs)  # noqa

        if 'staff' in self.required_roles and self.request.user.is_staff:
            return super(DesignPermissionMixin, self).dispatch(request, *args, **kwargs)  # noqa

        return HttpResponseForbidden()
