from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'status', 'created_at',
        'delivered_by_admin', 'cancelled_by_admin'
    )

    actions = ['admin_deliver', 'admin_cancel']

    # ✅ DELIVERY – anytime
    def admin_deliver(self, request, queryset):
        queryset.filter(
            status__in=['Pending', 'Confirmed']
        ).update(
            status='Delivered',
            delivered_by_admin=True
        )

    admin_deliver.short_description = "Deliver order (admin)"

    # ❌ CANCEL – only within 24h
    def admin_cancel(self, request, queryset):
        limit_time = timezone.now() - timedelta(hours=24)

        queryset.filter(
            created_at__gte=limit_time,
            status__in=['Pending', 'Confirmed']
        ).update(
            status='Cancelled',
            cancelled_by_admin=True
        )

    admin_cancel.short_description = "Cancel order (within 24h only)"