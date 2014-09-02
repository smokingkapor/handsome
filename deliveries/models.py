# -*- coding: utf-8 -*-
from django.db import models

from .constants import *  # noqa
from orders.models import Order


class Delivery(models.Model):

    DIRECTION_CHOICES = (
        (SEND, 'send'),
        (RETURN, 'return'),
    )
    order = models.ForeignKey(Order)
    direction = models.CharField(max_length=16, choices=DIRECTION_CHOICES,
                                 default=SEND)
    express_provider = models.CharField(max_length=64)
    express_code = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
