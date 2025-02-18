from django import template

register = template.Library()


@register.filter
def format_date(value):
    return value.strftime('%d.%m.%Y %H:%M')


@register.filter
def get_value(obj, key):
    return obj[key]
