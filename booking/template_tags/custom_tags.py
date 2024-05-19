
from django.template.defaulttags import register
from django import template

register = template.Library()


@register.simple_tag
def list_item(dict, key):
    return dict.get(key, {})