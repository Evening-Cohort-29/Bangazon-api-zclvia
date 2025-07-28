from django.db import models
from .customer import Customer
from .product import Product


class Like(models.Model):
  
  customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,)
  product = models.ForeignKey(Product, related_name='liked_product', on_delete=models.DO_NOTHING,)
