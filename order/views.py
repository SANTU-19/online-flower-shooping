from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('home')

    total = sum(item.total_price() for item in cart_items)
    return render(request, 'order/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def place_order(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

    payment_method = request.POST.get('payment')
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return JsonResponse({"success": False, "error": "Your cart is empty."})

    try:
        with transaction.atomic():
            total = sum(item.total_price() for item in cart_items)

            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                payment_method=payment_method,
                status='Confirmed' if payment_method == 'ONLINE' else 'Pending'
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart_items.delete()

        return JsonResponse({"success": True, "order_id": order.id})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

 
 

@login_required
def order_list(request):
    now = timezone.now()

    confirm_time = now - timedelta(minutes=30)
    deliver_time = now - timedelta(hours=24)

     
    Order.objects.filter(
        user=request.user,
        status='Pending',
        created_at__lte=confirm_time,
        cancelled_by_admin=False
    ).update(status='Confirmed')
 
    Order.objects.filter(
        user=request.user,
        status='Confirmed',
        cancelled_by_admin=False,
        delivered_by_admin=False,
        created_at__lte=deliver_time
    ).update(status='Delivered')

    
    current_orders = Order.objects.filter(
        user=request.user,
        status__in=['Pending', 'Confirmed']
    ).order_by('-created_at')

    
    history_orders = Order.objects.filter(
        user=request.user,
        status__in=['Delivered', 'Cancelled']
    ).order_by('-created_at')

    return render(request, 'order/orders.html', {
        'current_orders': current_orders,
        'history_orders': history_orders
    })
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    return render(request, 'order/order_detail.html', {
        'order': order,
        'items': items
    })