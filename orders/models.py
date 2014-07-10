# -*- coding: utf-8 -*-
from accounts.models import Profile
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import models
from django.db.models.signals import post_save

from .constants import(
    CREATED, PREPAID, DESIGNED, PAID, CANCELED, DONE, SENT,
    PRICE_299, PRICE_399, PRICE_499, PRICE_599, ACCEPTED, REFUNDING,
    REFUNDED, COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, COLOR_ORANGE,
    COLOR_COFFEE, COLOR_BLUE, COLOR_RED, COLOR_SILVER, HOBBY_READING,
    HOBBY_EXERCISE, HOBBY_SURF, HOBBY_OTHER
)


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
        (CREATED, u'等待支付预付款'),
        (PREPAID, u'设计师正在设计'),
        (DESIGNED, u'设计完成，等待确认'),
        (ACCEPTED, u'方案确认，等待支付尾款'),
        (PAID, u'支付完成，等待配送'),
        (SENT, u'等待收货'),
        (CANCELED, u'已取消'),
        (DONE, u'已完成'),
        (REFUNDING, u'退款中'),
        (REFUNDED, u'已退款'),
    )

    PRICE_CHOICES = (
        (PRICE_299, '299'),
        (PRICE_399, '399'),
        (PRICE_499, '499'),
        (PRICE_599, '599'),
    )

    COLOR_CHOICES = (
        (COLOR_WHITE, u'白色'),
        (COLOR_BLACK, u'黑色'),
        (COLOR_GRAY, u'灰色'),
        (COLOR_ORANGE, u'橙色'),
        (COLOR_COFFEE, u'咖啡色'),
        (COLOR_BLUE, u'蓝色'),
        (COLOR_RED, u'红色'),
        (COLOR_SILVER, u'银色'),
    )

    HOBBY_CHOICES = (
        (HOBBY_EXERCISE, u'运动'),
        (HOBBY_READING, u'看书'),
        (HOBBY_SURF, u'上网'),
        (HOBBY_OTHER, u'其他'),
    )

    code = models.CharField(max_length=32, unique=True, blank=True, null=True)
    total_price = models.FloatField(default=0)
    prepayment = models.FloatField()

    # address info
    address_province = models.ForeignKey(Province, null=True, blank=True)
    address_city = models.ForeignKey(City, null=True, blank=True)
    address_country = models.ForeignKey(Country, null=True, blank=True)
    house = models.CharField(max_length=256, blank=True)
    name = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64, blank=True)
    report = models.TextField(blank=True, null=True)

    # user requirements
    style = models.CharField(max_length=32, blank=True,
                             choices=Profile.STYLE_CHOICES)
    age_group = models.CharField(max_length=32, blank=True,
                                 choices=Profile.AGE_GROUP_CHOICES)
    price_group = models.FloatField(default=PRICE_299, choices=PRICE_CHOICES)
    color = models.CharField(max_length=32, default=COLOR_BLACK, choices=COLOR_CHOICES)
    hobby = models.CharField(max_length=32, default=HOBBY_OTHER, choices=HOBBY_CHOICES)
    height = models.CharField(max_length=16, blank=True)
    weight = models.CharField(max_length=16, blank=True)
    waistline = models.CharField(max_length=16, blank=True)
    chest = models.CharField(max_length=16, blank=True)
    hipline = models.CharField(max_length=16, blank=True)
    foot = models.CharField(max_length=16, blank=True)
    is_slim = models.BooleanField(default=False)
    preferred_designer = models.ForeignKey(User, related_name='designed_orders')  # noqa
    message = models.TextField(blank=True)

    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default=CREATED)
    express_info = models.CharField(max_length=128, blank=True)
    creator = models.ForeignKey(User, related_name='my_orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_address(self):
        region = self.address_province
        if self.address_city:
            region = u'{}{}'.format(region, self.address_city)
        if self.address_country:
            region = u'{}{}'.format(region, self.address_country)
        return u'{}{}'.format(region, self.house)

    def get_operations(self):
        """
        Get operation buttons for current order
        """
        operations = ''
        if self.status == CREATED:
            # prepay_url = reverse('orders:prepay', kwargs={'code': self.code})
            prepay_url = u'{}?code={}'.format(reverse('payments:home'), self.code)
            operations = '<a class="highlight" href="{}">支付预付款></a>'.format(prepay_url)
        elif self.status == ACCEPTED:
            # pay_url = reverse('orders:pay', kwargs={'code': self.code})
            pay_url = u'{}?code={}'.format(reverse('payments:home'), self.code)
            operations = '<a class="highlight" href="{}">支付尾款></a>'.format(pay_url)
        elif self.status == SENT:
            receive_url = reverse('orders:receive', kwargs={'code': self.code})
            operations = '<a class="highlight" href="{}">确认收货></a>'.format(receive_url)
        elif self.status == DESIGNED:
            choose_design_url = reverse('orders:detail', kwargs={'code': self.code})
            operations = '<a class="highlight" href="{}">挑选设计></a>'.format(choose_design_url)

        return operations

    def get_designer_operations(self):
        """
        Operations for designer
        """
        operations = ''
        if self.status == PREPAID:
            create_design_url = u'{}?code={}'.format(reverse_lazy('designs:create'), self.code)
            finish_design_url = reverse_lazy('orders:finish_design', kwargs={'code': self.code})
            operations = '<a class="highlight" href="{}">创建方案></a><br /><a class="highlight" href="{}">设计结束></a>'.format(create_design_url, finish_design_url)
        elif self.status == PAID:
            send_url = reverse('orders:send', kwargs={'code': self.code})
            operations = '<a class="highlight send-order-btn" href="javascript:void(0);" data-url="{}">已经寄出></a>'.format(send_url)
        return operations

    def __unicode__(self):
        return '{}\'s order'.format(self.creator.username)


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
