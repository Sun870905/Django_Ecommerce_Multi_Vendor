import random

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from apps.cart.cart import Cart

from .forms import AddToCartForm
from .models import Category, Product


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )
    context = {'products': products, 'query': query}
    return render(request, 'products/search.html', context)


def product(request, category_slug, product_slug):
    cart = Cart(request)
    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug
    )
    images_string = '{"thumbnail": "%s", "image": "%s","id": "main_image"},' % (
        product.get_thumbnail(),
        product.image.url
    )
    for image in product.images.all():
        images_string += '{"thumbnail": "%s", "image": "%s","id": "%s"},' % (
            image.get_thumbnail(),
            image.image.url,
            image.id
        )
    print(images_string)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(
                product_id=product.id,
                quantity=quantity,
                update_quantity=False
            )
            messages.success(request, 'Product successfully added to cart.')
            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()
    similar_products = list(product.category.products.exclude(id=product.id))
    if len(similar_products) == 4:
        similar_products = random.sample(similar_products, 4)
    context = {
        'product': product,
        'similar_products': similar_products,
        'form': form,
        'images_string': '[' + images_string.rstrip(',') + ']'
    }
    return render(request, 'products/detail.html', context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    context = {'category': category}
    return render(request, 'products/category_list.html', context)
