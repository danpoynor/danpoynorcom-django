from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join

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


@register.filter
def join_as_links(items, url_name):
    links = [format_html('<li><a href="{}">{}</a>{}</li>', reverse(url_name, args=[item.slug]), item.name, ',' if not item == items.last() else '') for item in items]
    return mark_safe(''.join(links))
