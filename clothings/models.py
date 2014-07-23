# -*- coding: utf-8 -*-
from django.db import models

from easy_thumbnails.fields import ThumbnailerImageField

from .constants import (
    T_SHIRT, SHIRT, POLO_SHIRT, JACKET, SUIT, KNITWEAR, WAISTCOAT,
    LEATHER_JACKET, COTTON_PADDED_CLOTHES, TWEED_COAT, FUR_CLOTHING,
    DOWN_COAT, DOWN_VEST, CASUAL_PANTS, JEANS, SUIT_PANTS, HAREM_PANTS
)


class Supplier(models.Model):
    """
    Clothing supplier model
    """
    name = models.CharField(u'名字', max_length=32)
    phone = models.CharField(u'联系电话', max_length=16, blank=True, null=True)
    security_code = models.CharField(u'代码', max_length=16, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


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

    supplier = models.ForeignKey(Supplier, blank=True, null=True, verbose_name=u'供应商')
    category = models.CharField(u'类别', max_length=64, choices=CATEGORY_CHOICES,
                                db_index=True)
    name = models.CharField(u'服装名', max_length=128)
    sku = models.CharField(u'库存编号', max_length=128, blank=True)
    price = models.FloatField(u'价格', )
    sizes = models.CharField(u'可选尺寸', max_length=128,
                             blank=True)  # separate with whitespace
    colors = models.CharField(u'可选颜色', max_length=128,
                              blank=True)  # separate with whitespace
    note = models.CharField(u'备注', max_length=256, blank=True)
    image = ThumbnailerImageField(
        upload_to='clothings',
        resize_source=dict(size=(1024, 1024), sharpen=True))
    is_active = models.BooleanField(u'有货', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
