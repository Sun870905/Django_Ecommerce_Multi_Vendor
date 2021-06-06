from django.urls import path

from .views import Success, cart_detail

urlpatterns = [
    path('', cart_detail, name='cart'),
    path('success/', Success.as_view(), name='success'),
]
