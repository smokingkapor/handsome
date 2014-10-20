# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    StaffuserRequiredMixin, AjaxResponseMixin, JSONResponseMixin
)

from .models import Promo


class PromoListView(StaffuserRequiredMixin, ListView):
    model = Promo


class CreatePromoView(StaffuserRequiredMixin, CreateView):
    model = Promo
    success_url = reverse_lazy('promos:list')


class UpdatePromoView(StaffuserRequiredMixin, UpdateView):
    model = Promo
    success_url = reverse_lazy('promos:list')


class VerifyPromoView(AjaxResponseMixin, JSONResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        if code:
            try:
                promo = Promo.objects.get(code=code)
                if promo.start_at > datetime.now().date():
                    return self.render_json_response({'available': False, 'reason': u'优惠码%s月%s日才能使用' % (promo.start_at.month, promo.start_at.day)})
                if promo.end_at < datetime.now().date():
                    return self.render_json_response({'available': False, 'reason': u'优惠码已过期'})
                return self.render_json_response({'available': True, 'discount': promo.discount})
            except Promo.DoesNotExist:
                return self.render_json_response({'available': False, 'reason': u'优惠码不存在'})
        return self.render_json_response({'available': False, 'reason': u'请输入优惠码'})
