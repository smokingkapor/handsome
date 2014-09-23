# -*- coding: utf-8 -*-
from django import template


register = template.Library()

@register.filter
def default_if_empty(value, arg):
    """
    Set default one if the value is empty.
    String: None, ''
    Integer: None, 0
    """
    if not value:
        return arg
    return value
