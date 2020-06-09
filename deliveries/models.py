from django.db import models
from staff.models import Staff
from branches.models import Branch
from supplier.models import Supplier
from products.models import Products
# Create your models here.

class Delivery(models.Model):

    date = models.DateTimeField(auto_now_add=True, unique=True)
    received_from = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    processed_by = models.ForeignKey(Staff, on_delete=models.PROTECT)
    value = models.FloatField(default=0.0)
    delivery_number = models.CharField(max_length=50, blank=True, null=True)
    is_transfer = models.BooleanField(default=False)



    class Meta:
        ordering = ["date",]

    def __str__(self):
        return self.received_from.name

    def get_absolute_url(self):
        return reverse("Delivery_detail", kwargs={"pk": self.pk})

class Stock(models.Model):

    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    posted = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0.0, help_text='Quantity received')
    buying_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    retail_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    wholesale_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    current_branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    home_branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='home_location', blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT)
    

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse("Stock_detail", kwargs={"pk": self.pk})

