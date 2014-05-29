# -*- coding: utf-8 -*-
from django.db import models

from .constants import (
    T_SHIRT, SHIRT, POLO_SHIRT, JACKET, SUIT, KNITWEAR, WAISTCOAT,
    LEATHER_JACKET, COTTON_PADDED_CLOTHES, TWEED_COAT, FUR_CLOTHING,
    DOWN_COAT, DOWN_VEST, CASUAL_PANTS, JEANS, SUIT_PANTS, HAREM_PANTS
)


class Clothing(models.Model):
    """
    Clothing model
    """
    CATEGORY_CHOICES = (
        (T_SHIRT, u'短袖'),
        (SHIRT, u'衬衫'),
        (POLO_SHIRT, u'POLO衫'),
        (JACKET, u'夹克'),
        (SUIT, u'西服'),
        (KNITWEAR, u'毛衣/针织衫'),
        (WAISTCOAT, u'马甲'),
        (LEATHER_JACKET, u'皮夹克'),
        (COTTON_PADDED_CLOTHES, u'棉衣'),
        (TWEED_COAT, u'呢大衣'),
        (FUR_CLOTHING, u'皮衣 '),
        (DOWN_COAT, u'羽绒服'),
        (DOWN_VEST, u'羽绒马甲'),

        (CASUAL_PANTS, u'休闲裤'),
        (JEANS, u'牛仔裤'),
        (SUIT_PANTS, u'西裤'),
        (HAREM_PANTS, u'哈伦裤'),
    )

    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES,
                                db_index=True)
    name = models.CharField(max_length=128)
    sku = models.CharField(max_length=128, blank=True)
    price = models.FloatField()
    sizes = models.CharField(max_length=128, blank=True)  # separate with comma
    colors = models.CharField(max_length=128, blank=True)  # separate with comma
    note = models.CharField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
