from django import template

register = template.Library()


@register.filter
def replace_underscore_with_space(value):
    return value.replace('_', ' ')


@register.filter
def replace_underscore_with_dash(value):
    return value.replace('_', '-')
