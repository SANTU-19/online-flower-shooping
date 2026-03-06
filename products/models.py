from django.db import models

# Create your models here.
 
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description=models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name