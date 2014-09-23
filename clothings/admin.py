# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Supplier, Clothing


admin.site.register(Supplier)
admin.site.register(Clothing)
