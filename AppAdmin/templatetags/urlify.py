
from django import template

register = template.Library()


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg


@register.filter(name='add')
def subtract(value, arg):
    return value + arg


@register.filter(name='multiple')
def multiple(value, arg):
    return value * arg


@register.filter(name='divide')
def multiple(value, arg):
    return value / arg

@register.filter(name='numberFormat')
def numberFormat(value):
    return format(int(value), ',d')

@register.filter()
def to_int(value):
    return int(value)

@register.filter(name='abs')
def abs_filter(value):
    return abs(value)

@register.filter(name='abs')
def str_underscore(value):
    return abs(value)

@register.filter
def minutes_diff(time_out, time_in):
    if time_out and time_in:
        return int((time_out - time_in).total_seconds() // 60)
    return 0

