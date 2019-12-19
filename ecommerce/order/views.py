from django.shortcuts import redirect, reverse
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from product.models import Variation
from utils import cart_total_quantity, cart_total
from .models import Order, OrderItem

class Pay(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'You need to login'
            )

            return redirect('user_profile:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart'
            )

            return redirect('product:list')

        cart = self.request.session.get('cart')
        cart_variation_ids = [variation for variation in cart]
        variations = list(
            Variation
                .objects
                .select_related('product')
                .filter(id__in=cart_variation_ids)
        )
        is_insufficient_stock = False

        for variation in variations:
            variation_id = str(variation.id)
            stock = variation.stock
            quantity_in_cart = cart[variation_id]['amount']
            price = cart[variation_id]['variation_price']
            promotional_price = cart[variation_id]['variation_promotional_price']

            if stock < quantity_in_cart:
                cart[variation_id]['amount'] = stock
                cart[variation_id]['quantitative_price'] = stock * price
                cart[variation_id]['promotional_quantitative_price'] = stock * promotional_price

                messages.error(
                    self.request,
                    f'Insufficient stock for {cart[variation_id]["product_name"]}'
                    f' {cart[variation_id]["variation_name"]} product.'
                    ' This product quantity has been changed.'
                )

                is_insufficient_stock = True

        if is_insufficient_stock:
            self.request.session.save()
            return redirect('product:cart')

        total = cart_total_quantity.cart_total_quantity(cart)
        total_amount = cart_total.cart_total(cart)

        order = Order(
            user=self.request.user,
            total=total,
            total_amount=total_amount,
            status='C'
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product_name=v['product_name'],
                    product_id=v['product_id'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    promotional_price=v['promotional_quantitative_price'],
                    quantity=v['amount'],
                    image=v['image']
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(
            reverse(
                'product:pay',
                kwargs={
                    'pk': order.pk
                }
            )   
        )

class SaveOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Save Order')

class Details(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Details')
