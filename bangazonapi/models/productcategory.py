from django.db import models


class ProductCategory(models.Model):

    name = models.CharField(max_length=55)

    class Meta:
        verbose_name = ("productcategory")
        verbose_name_plural = ("productcategories")