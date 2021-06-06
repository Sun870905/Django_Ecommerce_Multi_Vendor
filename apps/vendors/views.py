from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, DeleteView, ListView

from apps.products.models import Product

from .forms import ProductForm, ProductImageForm
from .models import Vendor


class VendorCreateView(CreateView):
    model = Vendor
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    context_object_name = 'form'
    template_name = "vendors/create.html"


@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()
    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True
        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False
    context = {'vendor': vendor, 'products': products, 'orders': orders}
    return render(request, 'vendors/detail.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()
            return redirect('vendor_admin')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'products/create.html', context)


@login_required
def edit_product(request, pk):
    vendor = request.user.vendor
    product = vendor.products.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            product_image = image_form.save(commit=False)
            product_image.product = product
            product_image.save()
            return redirect('vendor_admin')
        if form.is_valid():
            form.save()
            return redirect('vendor_admin')
    else:
        form = ProductForm(instance=product)
        image_form = ProductImageForm()
    context = {'form': form, 'product': product, 'image_form': image_form}
    return render(request, 'products/update.html', context)


@login_required
def edit_vendor(request):
    vendor = request.user.vendor
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        if name:
            vendor.created_by.email = email
            vendor.created_by.save()
            vendor.name = name
            vendor.save()
            return redirect('vendor_admin')
    context = {'vendor': vendor}
    return render(request, 'vendors/update.html', context)


class VendorListView(ListView):
    model = Vendor
    queryset = Vendor.objects.all()
    context_object_name = 'vendors'
    template_name = "vendors/list.html"


def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    context = {'vendor': vendor}
    return render(request, 'vendors/vendor.html', context)


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('vendor_admin')
    query_pk_and_slug = True
    template_name = "products/confirm_delete.html"
