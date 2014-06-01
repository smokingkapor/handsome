# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from easy_thumbnails.fields import ThumbnailerImageField

from .constants import(
    BUSINESS, CASUAL, ENGLAND, NO_IDEA, UNDER_20, BETWEEN_20_25, ABOVE_30,
    BETWEEN_25_30, FULL_BODY_SHOT
)


class Profile(models.Model):
    """
    User profile model
    """

    STYLE_CHOICES = (
        (BUSINESS, u'商务'),
        (CASUAL, u'休闲'),
        (ENGLAND, u'英伦'),
        (NO_IDEA, u'不知道'),
    )

    AGE_GROUP_CHOICES = (
        (UNDER_20, u'<20'),
        (BETWEEN_20_25, u'20-25'),
        (BETWEEN_25_30, u'25-30'),
        (ABOVE_30, u'>30'),
    )

    user = models.OneToOneField(User)
    avatar = ThumbnailerImageField(
        upload_to='avatars',
        default='avatars/default_avatar.png',
        resize_source=dict(size=(1024, 1024), sharpen=True))
    is_designer = models.BooleanField(default=False, db_index=True)
    preferred_style = models.CharField(max_length=32, blank=True,
                                       choices=STYLE_CHOICES)
    age_group = models.CharField(max_length=32, blank=True,
                                 choices=AGE_GROUP_CHOICES)
    height = models.CharField(max_length=16, blank=True)
    weight = models.CharField(max_length=16, blank=True)
    waistline = models.CharField(max_length=16, blank=True)
    chest = models.CharField(max_length=16, blank=True)
    hipline = models.CharField(max_length=16, blank=True)
    foot = models.CharField(max_length=16, blank=True)

    def get_fullbody_shot(self):
        photo = self.user.photo_set.filter(tag=FULL_BODY_SHOT, is_primary=True).first()  # noqa
        if photo:
            return photo.file
        return None

    def __unicode__(self):
        return ('designer - ' if self.is_designer else '') + self.user.username


class Photo(models.Model):
    """
    User photos
    """

    TAG_CHOICES = (
        (FULL_BODY_SHOT, u'全身照'),
    )

    user = models.ForeignKey(User)
    file = ThumbnailerImageField(
        upload_to='fullbody-shot',
        resize_source=dict(size=(1024, 1024), sharpen=True))
    is_primary = models.BooleanField(default=False)
    tag = models.CharField(max_length=16, choices=TAG_CHOICES,
                           default=FULL_BODY_SHOT, db_index=True)
    def __unicode__(self):
        return u'Photo {} for {}, primary?{}'.format(
            self.file, self.user.username,  self.is_primary)


def create_user_profile(sender, instance, created, **kwargs):
    """
    Create User profile when new User is added
    """
    if created:
        Profile(user=instance).save()

post_save.connect(create_user_profile, User)
