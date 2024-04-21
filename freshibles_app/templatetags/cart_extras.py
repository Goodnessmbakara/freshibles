# templatetags/cart_extras.py
from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies the value by the arg. Usage: {{ value|multiply:arg }}"""
    try:
        return value * arg
    except Exception as e:
        return ''

@register.filter(name='add')
def add(value, arg):
    """Adds the arg to the value. Usage: {{ value|add:arg }}"""
    try:
        return value + arg
    except Exception as e:
        return ''
