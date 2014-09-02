# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, Photo, DesignerWork


class DesignerWorkForm(forms.ModelForm):
    class Meta:
        model = DesignerWork

    def __init__(self, *args, **kwargs):
        super(DesignerWorkForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_staff=True)


class DesignerWorkAdmin(admin.ModelAdmin):
    form = DesignerWorkForm


class Staff(Profile):
    class Meta:
        proxy = True


class StaffAdmin(admin.ModelAdmin):
    def queryset(self, request):
        return self.model.objects.filter(user__is_staff=True)


admin.site.register(Profile)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Photo)
admin.site.register(DesignerWork, DesignerWorkAdmin)
