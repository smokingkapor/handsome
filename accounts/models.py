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

    STYLE_CHOICES = (
        (BUSINESS, u'商务'),
        (CASUAL, u'休闲'),
        (ENGLAND, u'英伦'),
        (NO_IDEA, u'其他'),
    )

    AGE_GROUP_CHOICES = (
        (AGE_GROUP_1, u'<23'),
        (AGE_GROUP_2, u'23-27'),
        (AGE_GROUP_3, u'28-33'),
        (AGE_GROUP_4, u'>33'),
    )

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

    SHOE_SIZE_CHOICES = (
        (SHOE_38, '38'),
        (SHOE_39, '39'),
        (SHOE_40, '40'),
        (SHOE_41, '41'),
        (SHOE_42, '42'),
        (SHOE_43, '43'),
        (SHOE_44, '44'),
        (SHOE_45, '45')
    )

    COLOR_CHOICES = (
        (BLACK, u'黑色'),
        (GRAY, u'灰色'),
    )

    PANTS_STYLE_CHOICES = (
        (CLOSE_FITTING, u'紧身'),
        (LOOSE, u'宽松'),
        (SLIM, u'修身')
    )

    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16, db_index=True, blank=True)
    avatar = ThumbnailerImageField(
        upload_to='avatars',
        default='avatars/default_avatar.png',
        resize_source=dict(size=(1024, 1024), sharpen=True))
    is_random_user = models.BooleanField(default=False)
    is_designer = models.BooleanField(default=False, db_index=True)
    age_group = models.CharField(max_length=32, blank=True,
                                 choices=AGE_GROUP_CHOICES)
    height = models.CharField(max_length=16, blank=True)
    weight = models.CharField(max_length=16, blank=True)
    color = models.CharField(max_length=16, blank=True, choices=COLOR_CHOICES)
    clothing_size = models.CharField(max_length=16, blank=True,
                                     choices=CLOTHING_SIZE_CHOICES)
    pants_size = models.CharField(max_length=16, blank=True,
                                  choices=PANTS_SIZE_CHOICES)
    pants_style = models.CharField(max_length=16, blank=True,
                                   choices=PANTS_STYLE_CHOICES)
    shoe_size = models.CharField(max_length=16, blank=True,
                                 choices=SHOE_SIZE_CHOICES)
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
