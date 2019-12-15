def cart_total_quantity(cart):
    return sum([item['amount'] for item in cart.values()])
