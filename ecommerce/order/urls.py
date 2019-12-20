from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('pay/<int:pk>', views.Pay.as_view(), name='pay'),
    path('save-order/', views.SaveOrder.as_view(), name='save_order'),
    path('details/', views.Details.as_view(), name='details'),
]
