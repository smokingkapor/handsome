# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import models
from django.db.models.signals import post_save

from .constants import(
    CREATED, PREPAID, DESIGNED, PAID, CANCELED, DONE, SENT,
    PRICE_299, PRICE_399, PRICE_499, PRICE_599
)
from accounts.models import Profile


class Order(models.Model):
    """
    Order model
    """
    STATUS_CHOICES = (
        (CREATED, u'等待支付定金'),
        (PREPAID, u'设计师正在设计'),
        (DESIGNED, u'设计完成，等待支付余款'),
        (PAID, u'支付完成，等待配送'),
        (SENT, u'等待收货'),
        (CANCELED, u'已取消'),
        (DONE, u'已完成'),
    )

    PRICE_CHOICES = (
        (PRICE_299, '299'),
        (PRICE_399, '399'),
        (PRICE_499, '499'),
        (PRICE_599, '599'),
    )


    code = models.CharField(max_length=32, unique=True, blank=True, null=True)
    total_price = models.FloatField(choices=PRICE_CHOICES)
    prepayment = models.FloatField()
    address = models.CharField(max_length=256)

    # user requirements
    style = models.CharField(max_length=32, blank=True,
                             choices=Profile.STYLE_CHOICES)
    age_group = models.CharField(max_length=32, blank=True,
                                 choices=Profile.AGE_GROUP_CHOICES)
    height = models.CharField(max_length=16, blank=True)
    weight = models.CharField(max_length=16, blank=True)
    waistline = models.CharField(max_length=16, blank=True)
    chest = models.CharField(max_length=16, blank=True)
    hipline = models.CharField(max_length=16, blank=True)
    foot = models.CharField(max_length=16, blank=True)
    preferred_designer = models.ForeignKey(User, related_name='designed_orders')  # noqa
    message = models.TextField()

    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default=CREATED)
    express_info = models.CharField(max_length=128, blank=True)
    creator = models.ForeignKey(User, related_name='my_orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_operations(self):
        """
        Get operation buttons for current order
        """
        operations = ''
        if self.status == CREATED:
            prepay_url = reverse('orders:prepay', kwargs={'code': self.code})
            operations = '<a href="{}">支付定金></a>'.format(prepay_url)
        elif self.status == DESIGNED:
            design = self.design_set.first()
            design_url = reverse('designs:detail', kwargs={'pk': design.id})
            pay_url = reverse('orders:pay', kwargs={'code': self.code})
            operations = '<a href="{}">设计方案></a><br /><a href="{}">支付尾款></a>'.format(design_url, pay_url)
        elif self.status == SENT:
            receive_url = reverse('orders:receive', kwargs={'code': self.code})
            operations = '<a href="{}">已经收到></a>'.format(receive_url)

        return operations

    def get_designer_operations(self):
        """
        Operations for designer
        """
        operations = ''
        if self.status == PREPAID:
            operations = '<a href="{}?order={}">创建方案></a>'.format(reverse_lazy('designs:create'), self.code)
        elif self.status == DESIGNED:
            design = self.design_set.first()
            design_url = reverse('designs:detail', kwargs={'pk': design.id})
            operations = '<a href="{}">查看方案></a>'.format(design_url)
        elif self.status == PAID:
            send_url = reverse('orders:send', kwargs={'code': self.code})
            operations = '<a href="javascript:void(0);" data-url="{}" class="send-order-btn">已经寄出></a>'.format(send_url)
        return operations

    def __unicode__(self):
        return '{}\'s order'.format(self.creator.username)


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


class Town(models.Model):
    """
    Town model
    """
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


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
