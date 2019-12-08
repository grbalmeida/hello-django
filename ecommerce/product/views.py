from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
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
