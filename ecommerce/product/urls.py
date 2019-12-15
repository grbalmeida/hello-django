from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductList.as_view(), name='list'),
    path('<slug>', views.ProductDetails.as_view(), name='details'),
    path('add-to-cart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('remove-from-cart/', views.RemoveFromCart.as_view(), name='remove_from_cart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('purchase-summary/', views.PurchaseSummary.as_view(), name='purchase_summary'),
]
