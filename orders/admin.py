# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Order, Province, City, Country


admin.site.register(Order)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Country)
