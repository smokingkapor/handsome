# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from .constants import CREATED, PREPAID, DESIGNED, PAID, CANCELED, DONE


class Order(models.Model):
    """
    Order model
    """
    STATUS_CHOICES = (
        (CREATED, u'等待支付定金'),
        (PREPAID, u'设计师正在设计'),
        (DESIGNED, u'设计完成，等待支付余款'),
        (PAID, u'支付完成，配送中'),
        (CANCELED, u'已取消'),
        (DONE, u'已完成'),
    )

    total_price = models.FloatField()
    prepayment = models.FloatField()
    address = models.CharField(max_length=256)

    # user requirements
    style = models.CharField(max_length=32, blank=True)
    age_group = models.CharField(max_length=32, blank=True)
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

    creator = models.ForeignKey(User, related_name='my_orders')
    created_at = models.DateTimeField(auto_now_add=True)


class Province(models.Model):
    """
    Province model
    """
    name = models.CharField(max_length=64)


class City(models.Model):
    """
    City model
    """
    province = models.ForeignKey(Province)
    name = models.CharField(max_length=64)


class Country(models.Model):
    """
    Country model
    """
    city = models.ForeignKey(City)
    name = models.CharField(max_length=64)


class Town(models.Model):
    """
    Town model
    """
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=64)
