# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from easy_thumbnails.fields import ThumbnailerImageField


from .constants import *  # noqa
from handsome.utils import path_and_rename


class Profile(models.Model):
    """
    User profile model
    """

    CLOTHING_SIZE_CHOICES = (
        (CLOTHING_S, 'S'),
        (CLOTHING_M, 'M'),
        (CLOTHING_L, 'L'),
        (CLOTHING_XL, 'XL'),
        (CLOTHING_XXL, 'XXL'),
        (CLOTHING_XXXL, 'XXXL')
    )

    PANTS_SIZE_CHOICES = (
        (PANTS_28, '28'),
        (PANTS_29, '29'),
        (PANTS_30, '30'),
        (PANTS_31, '31'),
        (PANTS_32, '32'),
        (PANTS_33, '33'),
        (PANTS_34, '34')
    )

    PANTS_STYLE_CHOICES = (
        (LOOSE, u'宽松型'),
        (SLIM, u'修身型'),
        (WHATEVER, u'都可以'),
    )

    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16, db_index=True, blank=True)
    avatar = ThumbnailerImageField(
        upload_to='avatars',
        default='avatars/default_avatar.png',
        resize_source=dict(size=(1024, 1024), sharpen=True))
    is_random_user = models.BooleanField(default=False)
    is_designer = models.BooleanField(default=False, db_index=True)
    age = models.CharField(max_length=16, blank=True)
    height = models.CharField(max_length=16, blank=True)
    weight = models.CharField(max_length=16, blank=True)
    clothing_size = models.CharField(max_length=16, blank=True,
                                     choices=CLOTHING_SIZE_CHOICES)
    pants_size = models.CharField(max_length=16, blank=True,
                                  choices=PANTS_SIZE_CHOICES)
    pants_style = models.CharField(max_length=16, blank=True,
                                   choices=PANTS_STYLE_CHOICES)
    is_freshman = models.BooleanField(default=True)
    intro = models.TextField(blank=True)
    qq = models.CharField(max_length=32, blank=True)

    def get_fullbody_shot(self):
        photo = self.user.photo_set.filter(tag=FULL_BODY_SHOT, is_primary=True).first()  # noqa
        if photo:
            return photo.file
        return None

    def __unicode__(self):
        return ('designer - ' if self.is_designer else '') + self.user.username


class DesignerWork(models.Model):
    user = models.ForeignKey(User)
    file = ThumbnailerImageField(
        upload_to=path_and_rename('designer-works'),
        resize_source=dict(size=(1024, 1024), sharpen=True))


class Photo(models.Model):
    """
    User photos
    """

    TAG_CHOICES = (
        (FULL_BODY_SHOT, u'全身照'),
    )

    user = models.ForeignKey(User)
    file = ThumbnailerImageField(
        upload_to=path_and_rename('fullbody-shot'),
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
