# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from .constants import(
    BUSINESS, CASUAL, ENGLAND, NO_IDEA, UNDER_20, BETWEEN_20_25, ABOVE_30,
    BETWEEN_25_30
)


class Profile(models.Model):
    """
    User profile model
    """

    STYLE_CHOICES = (
        (BUSINESS, '商务'),
        (CASUAL, '休闲'),
        (ENGLAND, '英伦'),
        (NO_IDEA, '不知道'),
    )

    AGE_GROUP_CHOICES = (
        (UNDER_20, '<20'),
        (BETWEEN_20_25, '20-25'),
        (BETWEEN_25_30, '25-30'),
        (ABOVE_30, '>30'),
    )

    user = models.OneToOneField(User)
    preferred_style = models.CharField(max_length=32, blank=True,
                                       choices=STYLE_CHOICES)
    age_group = models.CharField(max_length=32, blank=True,
                                 choices=AGE_GROUP_CHOICES)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    waistline = models.FloatField(blank=True, null=True)
    shoe_size = models.FloatField(blank=True, null=True)


def create_user_profile(sender, instance, created, **kwargs):
    """
    Create User profile when new User is added
    """
    if created:
        Profile(user=instance).save()

post_save.connect(create_user_profile, User)
