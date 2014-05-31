# -*- coding: utf-8 -*-
from django import forms

from .models import Design


class DesignForm(forms.ModelForm):
    """
    Model form for Design
    """
    selected_clothings = forms.CharField()
    photos = forms.CharField(required=False)

    class Meta:
        model = Design
        fields = ('comment',)
