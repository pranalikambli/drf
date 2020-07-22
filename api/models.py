from django.db import models

# Create your models here.


class Category(models.Model):
    class Meta:
        db_table = 'categories'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    subcategory_of = models.CharField(max_length=150, null=True, blank=True)
    parent_id = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


class Products(models.Model):
    class Meta:
        db_table = 'products'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=20, decimal_places=2, default = 0.0)
    is_active = models.BooleanField(default=True)

class ProductCategory(models.Model):
    class Meta:
        db_table = 'product_category'
        unique_together = (("product_id", "category_id"),)

    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    category_id = models.IntegerField()
