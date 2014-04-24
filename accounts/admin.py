# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Profile, Photo


admin.site.register(Profile)
admin.site.register(Photo)
