# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Design, DesignPhoto, DesignClothing


admin.site.register(Design)
admin.site.register(DesignPhoto)
admin.site.register(DesignClothing)
