from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    PAYMENT_CHOICES = (
        ('ONLINE', 'Online'),
        ('COD', 'Cash on Delivery'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    address = models.TextField(blank=True,null=True)   # 📍 DELIVERY LOCATION
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_by_admin=models.BooleanField(default=False)
    cancelled_by_admin=models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
