from django import template

register = template.Library()


@register.simple_tag
def verbose_name_plural(obj):
    return obj.get_verbose_name_plural()


@register.simple_tag
def verbose_name(obj):
    return obj.get_verbose_name()
