"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .settings.base import MEDIA_ROOT, MEDIA_URL

try:
    from .settings.local import DEBUG
except:
    from .settings.production import DEBUG

from .views import Contact, Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendors/', include('apps.vendors.urls')),
    path('cart/', include('apps.cart.urls')),
    path('', Home.as_view(), name='home'),
    path('contact/', Contact.as_view(), name='contact'),
    path('products/', include('apps.products.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]
