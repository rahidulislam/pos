from django.db import models

# Create your models here.
class Supplier(models.Model):

    name = models.CharField(max_length=250)
    supplier_code = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    primary_phone = models.CharField(max_length=15)
    secondary_phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    additional_email = models.EmailField(max_length=254, blank=True)
    address = models.TextField()
    additional_address = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Supplier_detail", kwargs={"pk": self.pk})
