# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.views.generic.base import View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from braces.views import(
    LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
    StaffuserRequiredMixin
)

from .constants import PREPAID, PAID, SENT, DONE
from .forms import CreateOrderForm
from .models import Order, Province, City, Address, Country
from accounts.models import Profile
from django.http.response import Http404
from designs.constants import SELECTED


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
        try:
            address = self.request.user.address_set.get(is_selected=True)
        except Address.DoesNotExist:
            address = None
        data.update({
            'address': address,
            'provinces': Province.objects.all()
        })
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

        # order address info
        address = Address.objects.get(id=self.request.REQUEST['address'])
        order.address_province = address.province
        order.address_city = address.city
        order.address_country = address.country
        order.house = address.house
        order.name = address.name
        order.phone = address.phone

        order.save()

        if self.request.is_ajax():
            url = reverse('orders:create_success', kwargs={'code': order.code})
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


class SaveAddressView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
                      View):
    """
    Save address info.
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Update or create a new one.
        """
        address_id = request.REQUEST.get('address_id')
        if address_id:
            address = Address.objects.get(id=address_id)
        else:
            address = Address(user=request.user)
        address.province = Province.objects.get(id=request.REQUEST['province'])
        try:
            address.city = City.objects.get(id=request.REQUEST.get('city'))
        except City.DoesNotExist:
            address.city = None
        try:
            address.country = Country.objects.get(id=request.REQUEST.get('country'))
        except Country.DoesNotExist:
            address.country = None
        address.house = request.REQUEST['house']
        address.name = request.REQUEST['name']
        address.phone = request.REQUEST['phone']
        address.save()
        return self.render_json_response({'id': address.id,
                                          'address': unicode(address)})


class CreateSuccessView(LoginRequiredMixin, DetailView):
    """
    Order create success page view
    """
    slug_field = 'code'
    slug_url_kwarg = 'code'
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


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Order detail page
    """
    slug_field = 'code'
    slug_url_kwarg = 'code'
    model = Order


class OrderListView(StaffuserRequiredMixin, ListView):
    """
    Designer is the staff. We display all the orders assigned to the designer.
    """
    model = Order

    def get_context_data(self, **kwargs):
        """
        Override. Add extra data to context
        """
        data = super(OrderListView, self).get_context_data(**kwargs)
        data.update({
            'STATUS_CHOICES': Order.STATUS_CHOICES,
            'AGE_GROUP_CHOICES': Profile.AGE_GROUP_CHOICES,
            'STYLE_CHOICES': Profile.STYLE_CHOICES
        })
        data.update(self.get_params_from_request())

        return data

    def get_params_from_request(self):
        """
        Get params from request GET
        """
        # status
        status = self.request.GET.get('status')
        status = status if status else 'all'

        # style
        style = self.request.GET.get('style')
        style = style if style else 'all'

        # age group
        age_group = self.request.GET.get('age-group')
        age_group = age_group if age_group else 'all'

        # created time
        try:
            created_from = self.request.GET.get('created-from')
            created_from_dt = datetime.strptime(created_from, '%m/%d/%Y')
        except:
            created_from_dt = None
        try:
            created_to = self.request.GET.get('created-to')
            created_to_dt = datetime.strptime(created_to, '%m/%d/%Y')
        except:
            created_to_dt = None

        return {'status': status, 'style': style, 'age_group': age_group,
                'created_from': created_from_dt, 'created_to': created_to_dt}

    def get_queryset(self):
        """
        Override. Filter the orders
        """
        qs = super(OrderListView, self).get_queryset()
        qs = qs.filter(preferred_designer=self.request.user)

        params = self.get_params_from_request()

        # status
        status = params['status']
        status_Q = Q(status=status) if status != 'all' else Q()

        # style
        style = params['style']
        style_Q = Q(style=style) if style != 'all' else Q()

        # age group
        age_group = params['age_group']
        age_group_Q = Q(age_group=age_group) if age_group != 'all' else Q()

        # created time
        from_dt = params['created_from']
        to_dt = params['created_to']
        created_time_Q = Q()
        if from_dt and to_dt:
            created_time_Q = Q(created_at__range=(from_dt, to_dt))
        elif from_dt:
            created_time_Q = Q(created_at__gte=from_dt)
        elif to_dt:
            created_time_Q = Q(created_at__lte=to_dt)

        qs = qs.filter(status_Q, style_Q, age_group_Q, created_time_Q)

        return qs.order_by('-created_at')


class PrepayView(LoginRequiredMixin, RedirectView):
    """
    Go to Alipay.
    Simply set the order to pre-paid now
    """
    permanent = False
    url = reverse_lazy('orders:me')

    def get_redirect_url(self, *args, **kwargs):
        """
        Update order status here
        """
        order = Order.objects.get(code=kwargs['code'])
        if order.creator != self.request.user:
            raise Http404
        order.status = PREPAID
        order.save()
        return super(PrepayView, self).get_redirect_url(*args, **kwargs)


class PayView(LoginRequiredMixin, RedirectView):
    """
    Go to Alipay.
    Simply set the order to paid now
    """
    permanent = False
    url = reverse_lazy('orders:me')

    def get_redirect_url(self, *args, **kwargs):
        """
        Update order status here
        """
        order = Order.objects.get(code=kwargs['code'])
        if order.creator != self.request.user:
            raise Http404
        order.status = PAID
        order.save()
        return super(PayView, self).get_redirect_url(*args, **kwargs)


class SendView(StaffuserRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
               View):
    """
    Send package.
    Simply set the order to sent now
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Update order here
        """
        order = Order.objects.get(code=kwargs['code'])
        order.status = SENT
        order.express_info = request.REQUEST['express_info']
        order.save()
        return self.render_json_response({'success': True})


class ReceiveView(LoginRequiredMixin, RedirectView):
    """
    The client receive the package
    Simply set the order to done now
    """
    permanent = False
    url = reverse_lazy('orders:me')

    def get_redirect_url(self, *args, **kwargs):
        """
        Update order status here
        """
        order = Order.objects.get(code=kwargs['code'])
        if order.creator != self.request.user:
            raise Http404
        order.status = DONE
        order.save()
        return super(ReceiveView, self).get_redirect_url(*args, **kwargs)


class OrderClothingsView(StaffuserRequiredMixin, TemplateView):
    """
    Display all the clothings for paid orders
    """
    template_name = 'orders/clothings.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(OrderClothingsView, self).get_context_data(**kwargs)
        design_clothings = []
        for order in Order.objects.filter(status=PAID):
            selected_design = order.design_set.get(status=SELECTED)
            design_clothings.extend(list(selected_design.clothings.all()))

        dcs_json = {}
        for design_clothing in design_clothings:
            dc_json = dcs_json.get(design_clothing.clothing.sku, {})
            dc_json['name'] = design_clothing.clothing.name
            key = u'{}、{}'.format(design_clothing.color, design_clothing.size)
            amount = dc_json.get('amount', {})
            count = amount.get(key, 0)
            amount[key] = count + 1
            dc_json['amount'] = amount
            dcs_json[design_clothing.clothing.sku] = dc_json

        data.update({'design_clothings': dcs_json})
        return data
