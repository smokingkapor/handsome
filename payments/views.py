# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponseForbidden, HttpResponse
from django.views.generic.base import RedirectView, TemplateView, View

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin

from .alipay import Alipay
from .constants import BANKS
from .models import Payment, Refund
from orders.constants import(
    PREPAID, PAID, CREATED, ACCEPTED, REFUNDING, REFUNDED
)
from orders.models import Order


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Payment select page.
    """
    template_name = 'payments/home.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(HomeView, self).get_context_data(**kwargs)
        order = Order.objects.get(code=self.request.GET['code'])
        if order.status not in [CREATED, ACCEPTED]:
            raise Http404()
        data.update({'BANKS': BANKS, 'order': order, 'CREATED': CREATED,
                     'ACCEPTED': ACCEPTED})
        return data


class PayView(LoginRequiredMixin, RedirectView):
    """
    Trigger alipay payment request
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Generate alipay request url
        """
        order = Order.objects.get(code=self.request.GET['code'])
        if order.status == CREATED:
            payment = 'advance'
            subject = u'优草预付款'
            total_fee = order.prepayment
        elif order.status == ACCEPTED:
            payment = 'final'
            subject = u'优草尾款'
            total_fee = order.total_price - order.prepayment
        else:
            raise Http404()
        site = get_current_site(self.request)

        alipay = Alipay(pid=settings.ALIPAY_PID, key=settings.ALIPAY_KEY,
                        seller_email=settings.ALIPAY_EMAIL)
        params = {
            'notify_url': u'http://{}{}'.format(site.domain, reverse('payments:notify')),
            'return_url': u'http://{}{}'.format(site.domain, reverse('payments:success')),
            'out_trade_no': '{}_{}'.format(order.code, payment),
            'subject': subject,
        }

        if settings.DEBUG:
            params.update({'total_fee': '0.01'})
        else:
            params.update({'total_fee': total_fee})

        bank = self.request.GET['bank']
        if bank != 'alipay':
            params.update({'defaultbank': bank, 'paymethod': 'bankPay'})

        return alipay.create_direct_pay_by_user_url(**params)


class SuccessView(LoginRequiredMixin, TemplateView):
    """
    Payment success.
    return_url for Alipay.
    """
    template_name = 'payments/success.html'

    def get(self, request, *args, **kwargs):
        """
        Verify notify
        """
        alipay = Alipay(pid=settings.ALIPAY_PID, key=settings.ALIPAY_KEY,
                        seller_email=settings.ALIPAY_EMAIL)
        if not alipay.verify_notify(**request.GET.dict()):
            return HttpResponseForbidden()
        code, payment_type = request.GET['out_trade_no'].split('_')
        order = Order.objects.get(code=code)
        payment = Payment()
        payment.buyer_id = request.GET.get('buyer_id')
        payment.buyer_email = request.GET.get('buyer_email')
        payment.trade_no = request.GET.get('trade_no')
        payment.trade_status = request.GET.get('trade_status')
        payment.full_content = json.dumps(request.GET.dict())
        payment.order = order
        payment.save()
        if payment.trade_status == 'TRADE_SUCCESS':
            if payment_type == 'advance' and order.status == CREATED:
                order.status = PREPAID
            elif payment_type == 'final' and order.status == ACCEPTED:
                order.status = PAID
            order.save()
        return super(SuccessView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add extra data to the context
        """
        data = super(SuccessView, self).get_context_data(**kwargs)
        code = self.request.GET['out_trade_no'].split('_')[0]
        order = Order.objects.get(code=code)
        data.update({'order': order, 'PREPAID': PREPAID, 'PAID': PAID})
        return data


class NotifyView(View):
    """
    notify_url for Alipay.
    Alipay will post the payment info to the server.
    Return 'success' to end the Alipay notification.
    """
    def post(self, request, *args, **kwargs):
        """
        Payment notify from alipay
        """
        alipay = Alipay(pid=settings.ALIPAY_PID, key=settings.ALIPAY_KEY,
                        seller_email=settings.ALIPAY_EMAIL)
        if not alipay.verify_notify(**request.POST.dict()):
            return HttpResponseForbidden()
        code, payment_type = request.GET['out_trade_no'].split('_')
        order = Order.objects.get(code=code)
        payment = Payment()
        payment.buyer_id = request.POST.get('buyer_id')
        payment.buyer_email = request.POST.get('buyer_email')
        payment.trade_no = request.POST.get('trade_no')
        payment.trade_status = request.POST.get('trade_status')
        payment.full_content = json.dumps(request.POST.dict())
        payment.order = order
        payment.save()
        if payment.trade_status == 'TRADE_SUCCESS':
            if payment_type == 'advance' and order.status == CREATED:
                order.status = PREPAID
            elif payment_type == 'final' and order.status == ACCEPTED:
                order.status = PAID
            order.save()
        return HttpResponse('success')


class RefundView(SuperuserRequiredMixin, RedirectView):
    """
    Refund the prepayment
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Refund the prepayment here.
        """

        alipay = Alipay(pid=settings.ALIPAY_PID, key=settings.ALIPAY_KEY,
                        seller_email=settings.ALIPAY_EMAIL)
        site = get_current_site(self.request)
        detail_data = []
        for order in Order.objects.filter(status=REFUNDING):
            payment = order.payment_set.filter(trade_status='TRADE_SUCCESS').first()
            refund = Refund(order=order, trade_no=payment.trade_no)
            refund.save()
            refund.batch_no = datetime.now().strftime('%Y%m%d') + str(refund.id).rjust(3, '0')
            refund.save()
            if settings.DEBUG:
                refund_amount = 0.01
            else:
                refund_amount = order.prepayment
            detail_data.append(u'{}^{}^{}'.format(payment.trade_no, refund_amount, u'用户主动申请退还预付款'))
        params = {
             'notify_url': u'http://{}{}'.format(site.domain, reverse('payments:refund_notify')),
             'refund_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
             'batch_no': refund.batch_no,
             'batch_num': 1,
             'detail_data': '#'.join(detail_data)
        }
        url = alipay._build_url('refund_fastpay_by_platform_pwd', **params)
        return url


class RefundNotifyView(View):
    """
    Refund notify from Alipay
    """
    def post(self, request, *args, **kwargs):
        """
        Payment notify from alipay
        """
        alipay = Alipay(pid=settings.ALIPAY_PID, key=settings.ALIPAY_KEY,
                        seller_email=settings.ALIPAY_EMAIL)
        if not alipay.verify_notify(**request.POST.dict()):
            return HttpResponseForbidden()
        refund = Refund.objects.get(batch_no=request.POST['batch_no'])
        refund.order.status = REFUNDED
        refund.order.save()
        return HttpResponse('success')
