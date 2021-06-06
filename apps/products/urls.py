from django.urls import path

from .views import category, product, search

urlpatterns = [
    path('search/', search, name='search'),
    path('<slug:category_slug>/<slug:product_slug>/', product, name='product'),
    path('<slug:category_slug>/', category, name='category'),
]
