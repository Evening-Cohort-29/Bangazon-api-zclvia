from django.db import models
from .customer import Customer


class Like(models.Model):
  
  customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,)
  product = models.ForeignKey("Product", related_name='liked_product', on_delete=models.DO_NOTHING,)
  
  class Meta:
    unique_together = 'customer', 'product'
