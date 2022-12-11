from django import template

register = template.Library()

@register.filter
def paginationhalf(value):
    half = float(value) / 2
    return int(half)

@register.filter
def paginationle1(value):
    return int(value)-1

@register.filter
def paginationle2(value):
    return int(value)-2