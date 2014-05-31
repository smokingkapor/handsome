# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from clothings.models import Clothing
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

    def __unicode__(self):
        return u'Design photo {} by {}'.format(self.file,
                                              self.designer.username)


class DesignClothing(models.Model):
    """
    Clothing for design
    """
    clothing = models.ForeignKey(Clothing)
    size = models.CharField(max_length=32)
    color = models.CharField(max_length=32)


class Design(models.Model):
    """
    Design proposal for the order
    """
    code = models.CharField(max_length=32, unique=True, blank=True, null=True)
    order = models.ForeignKey(Order)
    designer = models.ForeignKey(User, related_name='my_designs')
    client = models.ForeignKey(User, related_name='designs_for_me')
    is_selected = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    photos = models.ManyToManyField(DesignPhoto)
    clothings = models.ManyToManyField(DesignClothing)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Design for {} by {}'.format(self.client.username,
                                            self.designer.username)


def generate_design_code(sender, instance, created, *args, **kwargs):
    """
    Generate design code.
    100 + Date + Designer ID
    """
    if created:
        now = datetime.now().strftime('%y%m%d%H%M%S')
        instance.code = u'600{}{}'.format(now, instance.designer.id)
        instance.save(using=False)


post_save.connect(generate_design_code, Design)
