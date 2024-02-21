from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
    )

    user = models.ForeignKey(User, related_name='orders', null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=125)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED) 
    stripe_token = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-created_at',]

    def get_total_price(self):
        if self.paid_amount:
            return self.paid_amount

        return 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.price 
