# -*- coding: utf-8 -*-
from django import forms

from orders.models import Order


class CreateOrderForm(forms.ModelForm):
    """
    Model form for create order
    """
    class Meta:
        model = Order
        fields = ('total_price', 'message', 'preferred_designer')
