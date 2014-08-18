# -*- coding: utf-8 -*-
from django import forms

from orders.models import Order


class CreateOrderForm(forms.ModelForm):
    """
    Model form for create order
    """
    class Meta:
        model = Order
        fields = ('message', 'preferred_designer', 'age_group', 'price_group',
                  'style', 'height', 'weight', 'color', 'clothing_size',
                  'pants_size', 'pants_style', 'shoe_size', 'situation')


class FinishDesignForm(forms.Form):
    """
    Form for finish design and update the order status
    """
    report = forms.CharField(label=u'设计报告', widget=forms.Textarea)
