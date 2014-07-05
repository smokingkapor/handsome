# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from easy_thumbnails.fields import ThumbnailerImageField

from .constants import(
    BUSINESS, CASUAL, ENGLAND, NO_IDEA, AGE_GROUP_1, AGE_GROUP_2, AGE_GROUP_3,
    AGE_GROUP_4, FULL_BODY_SHOT
)


class Profile(models.Model):
    """
    User profile model
    """

    STYLE_CHOICES = (
        (BUSINESS, u'商务'),
        (CASUAL, u'休闲'),
        (ENGLAND, u'英伦'),
        (NO_IDEA, u'其他'),
    )

    AGE_GROUP_CHOICES = (
        (AGE_GROUP_1, u'<22'),
        (AGE_GROUP_2, u'23-27'),
        (AGE_GROUP_3, u'28-33'),
        (AGE_GROUP_4, u'>34'),
    )

    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16, db_index=True, blank=True)
    avatar = ThumbnailerImageField(
        upload_to='avatars',
        default='avatars/default_avatar.png',
        resize_source=dict(size=(1024, 1024), sharpen=True))
    is_random_user = models.BooleanField(default=False)
    is_designer = models.BooleanField(default=False, db_index=True)
    preferred_style = models.CharField(max_length=32, blank=True,
                                       choices=STYLE_CHOICES)
    age_group = models.CharField(max_length=32, blank=True,
                                 choices=AGE_GROUP_CHOICES)
    height = models.CharField(u'身高', max_length=16, blank=True)
    weight = models.CharField(u'体重', max_length=16, blank=True)
    waistline = models.CharField(u'腰围', max_length=16, blank=True)
    chest = models.CharField(u'胸围', max_length=16, blank=True)
    hipline = models.CharField(u'臀围', max_length=16, blank=True)
    foot = models.CharField(u'脚长', max_length=16, blank=True)
    is_freshman = models.BooleanField(default=True)

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
