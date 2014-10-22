# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import redirect
from django.views.generic.base import View, RedirectView, TemplateView,\
    TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from braces.views import(
    LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
    StaffuserRequiredMixin, SuperuserRequiredMixin
)

from .constants import *  # noqa
from .forms import CreateOrderForm, FinishDesignForm, AddressForm
from .mixins import OrderPermissionMixin
from .models import Order, Province, City, Address, Country
from accounts.models import Profile
from clothings.models import Supplier
from deliveries.constants import RETURN
from deliveries.models import Delivery
from designs.constants import SELECTED, WAITING, REJECTED
from designs.models import DesignClothing
from handsome.utils import send_sms
from orders.models import OrderClothing
from promos.models import Promo


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
        if self.request.GET.get('source') == 'one-key':
            # create order by one-key, pass the last order to the context
            data.update({'last_order': self.request.user.my_orders.last()})
        return data

    def form_valid(self, form):
        """
        Override. Set current user as creator. Return JSON if it's AJAX.
        """
        profile = self.request.user.profile

        order = form.save(commit=False)
        # order.prepayment = order.price_group * 0.1
        order.creator = profile.user
        profile.height = order.height
        profile.weight = order.weight
        profile.age_group = order.age_group
        profile.color = order.color
        profile.clothing_size = order.clothing_size
        profile.pants_size = order.pants_size
        profile.pants_style = order.pants_style
        profile.shoe_size = order.shoe_size
        profile.save()

        # order address info
        address = Address.objects.get(id=self.request.REQUEST['address'])
        order.address_province = address.province
        order.address_city = address.city
        order.address_country = address.country
        order.house = address.house
        order.name = address.name
        order.phone = address.phone

        order.save()

        # if the user is not freshman, they can simply create new order without
        # survey steps
        profile.is_freshman = False
        profile.save()

        if self.request.is_ajax():
            # url = u'{}?code={}'.format(reverse('payments:home'), order.code)
            url = reverse('orders:detail', kwargs={'code': order.code}) + '?mode=create'
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

        # set the phone to user profile
        request.user.profile.phone = request.REQUEST['phone']
        request.user.profile.save()

        return self.render_json_response({'id': address.id,
                                          'address': unicode(address)})


class UpdateAddressView(LoginRequiredMixin, FormView):
    template_name = 'orders/update_address.html'
    form_class = AddressForm

    def get_context_data(self, **kwargs):
        """
        Override. Add extra data to context
        """
        data = super(UpdateAddressView, self).get_context_data(**kwargs)
        try:
            address = self.request.user.address_set.get(is_selected=True)
        except Address.DoesNotExist:
            address = None
        data.update({
            'address': address,
            'provinces': Province.objects.all()
        })
        return data


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

    def get_context_data(self, **kwargs):
        data = super(MyOrderView, self).get_context_data(**kwargs)
        data.update({
            'CREATED': CREATED,
            'PREPAID': PREPAID,
            'SELECTED': SELECTED,
            'WAITING': WAITING,
            'REJECTED': REJECTED,
            'DESIGNED': DESIGNED,
            'SENT': SENT,
            'RETURNING': RETURNING,
        })
        data.update(self.request.GET.dict())
        return data

    def get_queryset(self):
        return self.request.user.my_orders.all().order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, OrderPermissionMixin, DetailView):
    """
    Order detail page
    """
    slug_field = 'code'
    slug_url_kwarg = 'code'
    model = Order

    def get_context_data(self, **kwargs):
        data = super(OrderDetailView, self).get_context_data(**kwargs)
        data.update({
            'CREATED': CREATED,
            'REDESIGN': REDESIGN,
            'PREPAID': PREPAID,
            'SELECTED': SELECTED,
            'WAITING': WAITING,
            'REJECTED': REJECTED,
            'DESIGNED': DESIGNED,
            'SENT': SENT,
            'RETURNING': RETURNING,
        })
        data.update(self.request.GET.dict())
        return data


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
            'STYLE_CHOICES': Profile.STYLE_CHOICES,
            'RETURNING': RETURNING,
            'REDESIGN': REDESIGN,
            'designers': Profile.objects.filter(user__is_staff=True,
                                                is_designer=True)
        })
        data.update(self.get_params_from_request())

        return data

    def get_params_from_request(self):
        """
        Get params from request GET
        """
        # designer
        designer = self.request.GET.get('designer')
        designer = designer if designer else 'all'

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
                'created_from': created_from_dt, 'created_to': created_to_dt,
                'designer': designer}

    def get_queryset(self):
        """
        Override. Filter the orders
        """
        qs = super(OrderListView, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(preferred_designer=self.request.user)

        params = self.get_params_from_request()

        # designer
        designer = params['designer']
        designer_Q = Q(preferred_designer__id=designer) if designer != 'all' else Q()

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

        qs = qs.filter(designer_Q, status_Q, style_Q, age_group_Q, created_time_Q)

        return qs.order_by('-created_at')


class PrepayView(LoginRequiredMixin, OrderPermissionMixin, RedirectView):
    """
    Go to Alipay.
    Simply set the order to pre-paid now
    """
    permanent = False
    url = reverse_lazy('orders:me')
    required_roles = ['owner']

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


class PayView(LoginRequiredMixin, OrderPermissionMixin, RedirectView):
    """
    Go to Alipay.
    Simply set the order to paid now
    """
    permanent = False
    url = reverse_lazy('orders:me')
    required_roles = ['owner']

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
        order.save()
        Delivery(order=order, express_provider=request.GET['express_provider'],
                 express_code=request.GET['express_code']).save()
        return self.render_json_response({'success': True})


class FinishDesignView(StaffuserRequiredMixin, FormView):
    """
    Update the order status to DESIGNED
    """
    template_name = 'orders/finish_design.html'
    form_class = FinishDesignForm

    def form_valid(self, form):
        """
        Save report and update order status
        """
        order = Order.objects.get(code=self.kwargs['code'])
        order.status = DESIGNED
        order.report = form.data['report']
        order.save()

        # send SMS notification
        name = self.request.user.get_full_name()
        name = name if name else self.request.user.username
        sms = settings.SMS_TEMPLATES['designed'].format(name)
        send_sms(order.phone, sms)
        return redirect(reverse('orders:detail', kwargs={'code': order.code}))


class ReceiveView(LoginRequiredMixin, OrderPermissionMixin, RedirectView):
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


class OrderClothingsView(SuperuserRequiredMixin, TemplateView):
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
            design_clothings.extend(list(selected_design.clothings.filter(wanted=True)))  # noqa

        dcs_json = {}
        for design_clothing in design_clothings:
            dc_json = dcs_json.get(design_clothing.clothing.sku, {})
            dc_json['name'] = design_clothing.clothing.name
            dc_json['supplier'] = design_clothing.clothing.supplier.name
            key = u'{}/{}'.format(design_clothing.color, design_clothing.size)
            amount = dc_json.get('amount', {})
            count = amount.get(key, 0)
            amount[key] = count + 1
            dc_json['amount'] = amount
            dcs_json[design_clothing.clothing.sku] = dc_json

        data.update({'design_clothings': dcs_json})
        return data


class OrderSupplierClothingsView(TemplateResponseMixin, View):
    """
    Display all the clothings the supplier need to send to us.
    """
    template_name = 'orders/supplier_clothings.html'

    def dispatch(self, request, *args, **kwargs):
        code = request.POST.get('code')
        if code:
            try:
                supplier = Supplier.objects.get(security_code=code)
            except Supplier.DoesNotExist:
                return self.render_to_response({'code': code, 'error': True})
            design_clothings = []
            for order in Order.objects.filter(status=PAID):
                selected_design = order.design_set.get(status=SELECTED)
                design_clothings.extend(list(selected_design.clothings.filter(wanted=True)))  # noqa

            dcs_json = {}
            for design_clothing in design_clothings:
                if design_clothing.clothing.supplier == supplier:
                    dc_json = dcs_json.get(design_clothing.clothing.sku, {})
                    dc_json['name'] = design_clothing.clothing.name
                    key = u'{}/{}'.format(design_clothing.color, design_clothing.size)
                    amount = dc_json.get('amount', {})
                    count = amount.get(key, 0)
                    amount[key] = count + 1
                    dc_json['amount'] = amount
                    dcs_json[design_clothing.clothing.sku] = dc_json
            return self.render_to_response({'design_clothings': dcs_json,
                                            'code': code})
        else:
            return self.render_to_response({'code': code})


class RefundView(LoginRequiredMixin, OrderPermissionMixin, RedirectView):
    """
    User request for refund the prepayment
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Update order status here
        """
        order = Order.objects.get(code=kwargs['code'])
        if order.status in [PREPAID, DESIGNED, ACCEPTED]:
            order.status = REFUNDING
            order.save()
        else:
            raise Http404()
        return reverse('orders:detail', kwargs={'code': order.code})


class SelectClothingView(LoginRequiredMixin, RedirectView):
    """
    Select clothings and update the order status
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Update order here
        """
        order = Order.objects.get(code=kwargs['code'])
        if self.request.user != order.creator:
            raise Http404
        ids = self.request.GET['ids'].split(',')
        total_price = 0
        for design_clothing in DesignClothing.objects.in_bulk(ids).values():
            total_price += design_clothing.clothing.price
            OrderClothing.objects.get_or_create(
                order=order, design_clothing=design_clothing,
                design=design_clothing.design_set.first())
        order.status = ACCEPTED
        order.total_price = total_price
        try:
            order.promo = Promo.objects.get(code=self.request.GET.get('promo_code'))
        except:
            pass
        order.save()
        return '{}?code={}'.format(reverse('payments:home'), order.code)


class ReturnView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin,
                 View):

    def post_ajax(self, request, *args, **kwargs):
        order = Order.objects.get(code=request.GET['code'])
        if self.request.user != order.creator:
            raise Http404

        order.status = RETURNING
        order.save()
        Delivery(order=order,
                 express_provider=request.POST['express_provider'],
                 express_code=request.POST['express_code'],
                 reason=request.POST['reason'],
                 direction=RETURN).save()
        return self.render_json_response({'success': True})


class ReceiveReturnView(StaffuserRequiredMixin, RedirectView):
    permanent = False
    url = reverse_lazy('orders:list')

    def get_redirect_url(self, *args, **kwargs):
        """
        Update order status here
        """
        order = Order.objects.get(code=kwargs['code'])
        order.status = REFUNDING
        order.save()
        return super(ReceiveReturnView, self).get_redirect_url(*args, **kwargs)


class RedesignView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(code=self.kwargs['code'])
        if self.request.user != order.creator or order.status != DESIGNED:
            raise Http404

        order.status = REDESIGN
        order.redesign_reason = request.POST.get('reason', '')
        order.save()
        return redirect('orders:me')
