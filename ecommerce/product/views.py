from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from pprint import pprint
from . import models

class ProductList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductDetails(DetailView):
    model = models.Product
    template_name = 'product/details.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )

        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'Product not found'
            )

            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)
        product = variation.product

        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        variation_stock = variation.stock
        variation_price = variation.price
        variation_promotional_price = variation.promotional_price
        amount = 1
        slug = product.slug

        image = product.image
        image = image.name if image else ''

        if variation.stock < 1:
            messages.error(
                self.request,
                'Insufficient stock'
            )

            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session.get('cart')

        if variation_id in cart:
            current_amount = cart[variation_id]['amount']
            current_amount += 1

            if variation_stock < current_amount:
                messages.warning(
                    self.request,
                    f'Insufficient stock for {current_amount}x in {product_name} product. '
                    f'We add {variation_stock}x to your cart.'
                )

                current_amount = variation_stock

            cart[variation_id]['amount'] = current_amount
            cart[variation_id]['quantitative_price'] = variation_price * current_amount
            cart[variation_id]['promotional_quantitative_price'] = \
                variation_promotional_price * current_amount
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_id': variation_id,
                'variation_name': variation_name,
                'variation_price': variation_price,
                'variation_promotional_price': variation_promotional_price,
                'quantitative_price': variation_price,
                'promotional_quantitative_price': variation_promotional_price,
                'amount': amount,
                'slug': slug,
                'image': image
            }

        self.request.session.save()
        # pprint(cart)

        messages.success(
            self.request,
            f'{product_name} {variation_name} product added to your cart'
        )

        return redirect(http_referer)

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remove from Cart')

class Cart(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/cart.html')

class FinalizeOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalize Order')
