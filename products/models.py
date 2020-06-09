from django.db import models
from staff.models import Staff
from supplier.models import Supplier
from branches.models import Branch
# Create your models here.

class Products(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=300, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sku_code = models.CharField(max_length=50, unique=True)
    product_image = models.ImageField(upload_to='product_image/', blank=True)
    quantity = models.IntegerField(default=0, help_text='Quantity in stock')
    buying_price = models.DecimalField( max_digits=9, decimal_places=2, default=0.00)
    retail_price = models.DecimalField( max_digits=9, decimal_places=2, default=0.00)
    wholesale_price = models.DecimalField( max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Products_detail", kwargs={"pk": self.pk})

class BranchProduct(models.Model):

    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse("BranchProduct_detail", kwargs={"pk": self.pk})

class Transfer(models.Model):

    transfer_from = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='transfer_from')
    transfer_to = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='transfer_to')
    transfer_date = models.DateTimeField(auto_now_add=True)
    date_received = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    value = models.FloatField(default=0.0)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        permissions = [('receive_transfer', 'Can receive transfer')]

    def __str__(self):
        return str(self.transfer_date)

    def get_products(self):
        pass

    def get_absolute_url(self):
        return reverse("Transfer_detail", kwargs={"pk": self.pk})

class TransferProduct(models.Model):

    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    transfer = models.ForeignKey(Transfer, on_delete=models.PROTECT)
    unit_cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse("TransferProduct_detail", kwargs={"pk": self.pk})



