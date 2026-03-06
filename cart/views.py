from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.http import JsonResponse

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    total_quantity = sum(
        item.quantity for item in Cart.objects.filter(user=request.user)
    )

    return JsonResponse({'cart_count': total_quantity})


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    item.delete()
    return redirect('view_cart')
@login_required
def increase_qty(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('view_cart')


@login_required
def decrease_qty(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('view_cart')
