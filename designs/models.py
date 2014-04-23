# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from orders.models import Order


class DesignPhoto(models.Model):
    """
    Photo for design
    """
    designer = models.ForeignKey(User)
    file = models.CharField(max_length=64)
    description = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '{}design-photo/{}'.format(settings.MEDIA_URL, self.file)


class Design(models.Model):
    """
    Design proposal for the order
    """
    order = models.ForeignKey(Order)
    designer = models.ForeignKey(User, related_name='my_designs')
    client = models.ForeignKey(User, related_name='designs_for_me')
    is_selected = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    photos = models.ManyToManyField(DesignPhoto)
    created_at = models.DateTimeField(auto_now_add=True)
