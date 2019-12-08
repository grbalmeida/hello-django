from django.template import Library
from utils import format_price

register = Library()

@register.filter
def currency_filter(value):
    return format_price.format_price(value)