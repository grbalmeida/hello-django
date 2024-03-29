from django.template import Library
from utils import format_price, cart_total_quantity, cart_total

register = Library()

@register.filter
def currency_filter(value):
    return format_price.format_price(value)

@register.filter
def cart_total_quantity_filter(cart):
    return cart_total_quantity.cart_total_quantity(cart)

@register.filter
def cart_total_filter(cart):
    return cart_total.cart_total(cart)
