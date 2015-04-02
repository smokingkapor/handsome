# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import models
from django.db.models.signals import post_save

from .constants import *  # noqa
from accounts.models import Profile
from promos.models import Promo


class Province(models.Model):
    """
    Province model
    """
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class City(models.Model):
    """
    City model
    """
    province = models.ForeignKey(Province)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    """
    Country model
    """
    city = models.ForeignKey(City)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Address(models.Model):
    """
    Address for user
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64, blank=True)
    province = models.ForeignKey(Province)
    city = models.ForeignKey(City, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    house = models.CharField(max_length=256, blank=True)
    is_selected = models.BooleanField(default=True)

    def get_region(self):
        region = self.province
        if self.city:
            region = u'{}{}'.format(region, self.city)
        if self.country:
            region = u'{}{}'.format(region, self.country)
        return region

    def __unicode__(self):
        return u'{}, {} {}, {}'.format(self.name, self.get_region(),
                                       self.house, self.phone)


class Order(models.Model):
    """
    Order model
    """
    STATUS_CHOICES = (
        (CREATED, u'正在设计'),
        # (CREATED, u'等待支付预付款'),
        # (PREPAID, u'正在设计'),
        (DESIGNED, u'等待您选择'),
        (REDESIGN, u'重新设计'),
        (ACCEPTED, u'等待支付'),
        (PAID, u'正在配送'),
        (SENT, u'已发货'),
        (CANCELED, u'已取消'),
        (DONE, u'已完成'),
        (REFUNDING, u'正在退款'),
        (REFUNDED, u'已退款'),
        (RETURNING, u'正在退货'),
    )

    SITUATION_CHOICES = (
        (SITUATION_WORK, u'职场着装'),
        (SITUATION_BUSINESS, u'商务着装'),
        (SITUATION_DAILY, u'日常着装'),
        (SITUATION_OTHER, u'其他'),
    )

    code = models.CharField(max_length=32, unique=True, blank=True, null=True)
    total_price = models.FloatField(default=0)
    prepayment = models.FloatField(default=0)

    # address info
    address_province = models.ForeignKey(Province, null=True, blank=True)
    address_city = models.ForeignKey(City, null=True, blank=True)
    address_country = models.ForeignKey(Country, null=True, blank=True)
    house = models.CharField(max_length=256, blank=True)
    name = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64, blank=True)
    report = models.TextField(blank=True, null=True)

    # user requirements
    age = models.CharField(max_length=32, blank=True)
    price_group = models.FloatField()
    height = models.CharField(max_length=16, blank=True)
    weight = models.CharField(max_length=16, blank=True)
    clothing_size = models.CharField(max_length=16, blank=True,
                                     choices=Profile.CLOTHING_SIZE_CHOICES)
    pants_size = models.CharField(max_length=16, blank=True,
                                  choices=Profile.PANTS_SIZE_CHOICES)
    pants_style = models.CharField(max_length=16, blank=True,
                                   choices=Profile.PANTS_STYLE_CHOICES)
    preferred_designer = models.ForeignKey(User, related_name='designed_orders',
                                           blank=True, null=True)  # noqa
    message = models.TextField(blank=True)

    situation = models.CharField(max_length=16, choices=SITUATION_CHOICES,
                                 blank=True, null=True)
    usual_dress = models.TextField(blank=True)
    preferred_dress = models.TextField(blank=True)

    promo = models.ForeignKey(Promo, blank=True, null=True)
    redesign_reason = models.TextField(default='')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default=CREATED)
    creator = models.ForeignKey(User, related_name='my_orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_address(self):
        region = self.address_province
        if self.address_city:
            region = u'{}{}'.format(region, self.address_city)
        if self.address_country:
            region = u'{}{}'.format(region, self.address_country)
        return u'{}{}'.format(region, self.house)

    def get_usual_dress_display(self):
        try:
            return ','.join([Profile.USUAL_DRESS_OPTIONS[str(val)] for val in json.loads(self.usual_dress)])
        except:
            return ''

    def get_preferred_dress_display(self):
        try:
            return ','.join([Profile.PREFERRED_DRESS_OPTIONS[str(val)] for val in json.loads(self.preferred_dress)])
        except:
            return ''

    def get_operations(self):
        """
        Get operation buttons for current order
        """
        operations = ''
        #         if self.status == CREATED:
        #             # prepay_url = reverse('orders:prepay', kwargs={'code': self.code})
        #             prepay_url = u'{}?code={}'.format(reverse('payments:home'), self.code)
        #             operations = u'<a href="{}">支付预付款</a>'.format(prepay_url)
        if self.status == ACCEPTED:
            # pay_url = reverse('orders:pay', kwargs={'code': self.code})
            pay_url = u'{}?code={}'.format(reverse('payments:home'), self.code)
            operations = u'<a class="btn btn-sm btn-operation" href="{}">支付</a>'.format(pay_url)
        elif self.status == SENT:
            receive_url = reverse('orders:receive', kwargs={'code': self.code})
            operations = u'<a class="btn btn-sm btn-operation" href="{}">确认收货</a>'.format(receive_url)
        elif self.status == DESIGNED:
            choose_design_url = reverse('orders:detail', kwargs={'code': self.code})
            operations = u'<a class="btn btn-sm btn-operation" href="{}">挑选设计</a>'.format(choose_design_url)
        elif self.status in [SENT, DONE]:
            return_url = '{}?code={}'.format(reverse('orders:return'), self.code)
            operations = u'<a class="btn btn-sm btn-operation" href="javascript:void(0)" class="return-btn" data-url="{}">申请退货</a>'.format(return_url)

        return operations

    def get_designer_operations(self):
        """
        Operations for designer
        """
        operations = ''
        if self.status in [CREATED, REDESIGN]:
            create_design_url = u'{}?code={}'.format(reverse_lazy('designs:create'), self.code)
            finish_design_url = reverse_lazy('orders:finish_design', kwargs={'code': self.code})
            operations = '<a class="highlight" href="{}">创建方案></a> <a class="highlight" href="{}">设计结束></a>'.format(create_design_url, finish_design_url)
        elif self.status == DESIGNED:
            create_design_url = u'{}?code={}'.format(reverse_lazy('designs:create'), self.code)
            operations = '<a class="highlight" href="{}">创建方案></a>'.format(create_design_url)
        elif self.status == PAID:
            send_url = reverse('orders:send', kwargs={'code': self.code})
            operations = '<a class="highlight send-order-btn" href="javascript:void(0);" data-url="{}">已经寄出></a>'.format(send_url)
        elif self.status == RETURNING:
            receive_return_url = reverse('orders:receive_return', kwargs={'code': self.code})
            operations = '<a class="highlight" href="{}">收到退货></a>'.format(receive_return_url)
        return operations

    @property
    def final_price(self):
        if self.promo:
            return self.total_price * self.promo.discount
        return self.total_price

    @property
    def discount(self):
        if self.promo:
            return self.total_price * (1-self.promo.discount)
        return 0

    @property
    def express_info(self):
        delivery = self.delivery_set.order_by('-id').first()
        if delivery:
            if delivery.reason:
                return u'{} {}. <br />原因: {}'.format(
                    delivery.express_provider,
                    delivery.express_code,
                    delivery.reason)
            return u'{} {}'.format(delivery.express_provider, delivery.express_code)
        else:
            return u'暂时没有快递信息'

    def __unicode__(self):
        return u'{}\'s order'.format(self.creator.username)


class OrderClothing(models.Model):
    """
    Selected clothing for the order
    """
    order = models.ForeignKey(Order)
    design = models.ForeignKey('designs.Design', blank=True, null=True)
    design_clothing = models.ForeignKey('designs.DesignClothing')


def generate_order_code(sender, instance, created, *args, **kwargs):
    """
    Generate order code.
    600 + Date + User ID
    """
    if created:
        now = datetime.now().strftime('%y%m%d%H%M%S')
        instance.code = u'600{}{}'.format(now, instance.creator.id)
        instance.save(using=False)


post_save.connect(generate_order_code, Order)
