from django import template

register = template.Library()


@register.filter
def replace_underscore_with_space(value):
    return value.replace('_', ' ')


@register.filter
def replace_underscore_with_dash(value):
    return value.replace('_', '-')


@register.filter
def next_item(items, i):
    return items[i + 1].slug if i < len(items) - 1 else items.first().slug


@register.filter
def previous_item(items, i):
    return items[i - 1].slug if i > 0 else items.last().slug


@register.filter
def class_name(value):
    return value.__class__.__name__
