# -*- coding: utf-8 -*-
from django.db import models

from orders.models import Order


class Payment(models.Model):
    """
    Payment info returned from Alipay
    """
    order = models.ForeignKey(Order)
    trade_no = models.CharField(max_length=64)
    trade_status = models.CharField(max_length=64)
    buyer_id = models.CharField(max_length=32)
    buyer_email = models.CharField(max_length=128)
    full_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Refund(models.Model):
    """
    Refund prepayment
    """
    batch_no = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    order = models.ForeignKey(Order)
    trade_no = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
