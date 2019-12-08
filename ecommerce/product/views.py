from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class ProductList(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Product List')

class ProductDetails(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Product Details')

class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Add to Cart')

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remove from Cart')

class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')

class FinalizeOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalize Order')
