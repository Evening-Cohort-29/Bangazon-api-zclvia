from django.contrib.auth.models import User
from django.db import models

from .customer import Customer


class Store(models.Model):
    """Store model representing a seller's store"""

    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="store"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_date = models.DateField(auto_now_add=True)

    @property
    def seller_name(self):
        """Full name of the store owner"""
        return f"{self.customer.user.first_name} {self.customer.user.last_name}"

    @property
    def product_count(self):
        """Count of products currently for sale in this store"""
        return self.customer.products.count()

    def __str__(self):
        return self.name
