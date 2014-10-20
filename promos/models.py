# -*- coding: utf-8 -*-
from django.db import models


class Promo(models.Model):
    code = models.CharField(max_length=16, unique=True)
    discount = models.FloatField()
    start_at = models.DateField()
    end_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
