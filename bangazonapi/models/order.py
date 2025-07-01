"""Customer order model"""
from django.db import models
from .customer import Customer
from .payment import Payment


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,)
    payment_type = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True)
    created_date = models.DateField(default="0000-00-00",)
