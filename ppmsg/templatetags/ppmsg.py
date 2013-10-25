# -*- coding: utf-8 -*-
from django import template
from django.template import Context

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)