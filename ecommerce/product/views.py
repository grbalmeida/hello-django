from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from user_profile.models import UserProfile, Address

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

        messages.success(
            self.request,
            f'{product_name} {variation_name} product added to your cart'
        )

        return redirect(http_referer)

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )

        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        cart = self.request.session.get('cart')

        if not cart:
            return redirect(http_referer)

        if variation_id not in cart:
            return redirect(http_referer)

        messages.success(
            self.request,
            f'Product {cart[variation_id]["product_name"]} '
            f'{cart[variation_id]["variation_name"]} removed from your cart'
        )

        del cart[variation_id]
        self.request.session.save()

        return redirect(http_referer)

class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart')
        }

        return render(self.request, 'product/cart.html', context)

class PurchaseSummary(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_profile:create')

        user_profile_exists = UserProfile.objects.filter(user=self.request.user).exists()
        user_profile = UserProfile.objects.get(user=self.request.user)
        address = Address.objects.get(user_profile=user_profile)

        if not user_profile_exists:
            messages.error(
                self.request,
                'User without profile'
            )

            return redirect('user_profile:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart'
            )

            return redirect('product:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
            'address': address,
            'user_profile': user_profile
        }

        return render(self.request, 'product/purchase-summary.html', context)
