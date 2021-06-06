from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (ProductDeleteView, VendorCreateView, VendorListView,
                    add_product, edit_product, edit_vendor, vendor,
                    vendor_admin)

urlpatterns = [
    path('become-vendor/', VendorCreateView.as_view(), name='become_vendor'),
    path('vendor-admin/', vendor_admin, name='vendor_admin'),
    path('add-product/', add_product, name='add_product'),
    path('edit-vendor/', edit_vendor, name='edit_vendor'),
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),
    path('delete-product/<int:pk>/',
         ProductDeleteView.as_view(), name='delete_product'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='vendors/login.html'), name='login'),
    path('', VendorListView.as_view(), name='vendors'),
    path('<int:vendor_id>/', vendor, name='vendor')
]
