from django import template
from datetime import datetime

register = template.Library()

@register.filter
def sum_prices(cart_items):
    return sum(item.price for item in cart_items)


@register.filter
def date_difference(start_date, end_date):
    return (end_date - start_date).days

@register.filter
def total_price(item):
    days = (item.end_date - item.start_date).days
    return item.quantity * item.product.product_price_per_day * days

@register.filter
def sum_order_prices(orders):
    return sum(order.price for order in orders)