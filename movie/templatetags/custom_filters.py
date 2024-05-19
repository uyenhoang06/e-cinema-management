from django import template

register = template.Library()

@register.filter(name='active1')
def active1(value):
    return 'active' if value == 0 else ''