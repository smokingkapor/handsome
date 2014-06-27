# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Payment, Refund


admin.site.register(Payment)
admin.site.register(Refund)
