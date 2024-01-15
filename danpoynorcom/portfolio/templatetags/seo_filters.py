from django import template

register = template.Library()


@register.filter
def first_part(value, arg):
    return value[:arg]


@register.filter
def excess_part(value, arg):
    return value[arg:]
