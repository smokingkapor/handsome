# -*- coding: utf-8 -*-
from django import forms

from orders.models import Order, Address


class CreateOrderForm(forms.ModelForm):
    """
    Model form for create order
    """
    class Meta:
        model = Order
        fields = ('message', 'preferred_designer', 'age', 'price_group',
                  'problem', 'height', 'weight', 'clothing_size',
                  'pants_size', 'pants_style',)


class FinishDesignForm(forms.Form):
    """
    Form for finish design and update the order status
    """
    report = forms.CharField(label=u'设计报告', widget=forms.Textarea)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'is_selected')
