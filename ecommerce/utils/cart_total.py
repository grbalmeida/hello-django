def cart_total(cart):
    return sum(
        [
            item.get('promotional_quantitative_price')
            if item.get('promotional_quantitative_price')
            else item.get('quantitative_price')
            for item
            in cart.values()
        ]
    )
