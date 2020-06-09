from django.db import models

# Create your models here.
class Customer(models.Model):
    """Model definition for Customer."""

    name = models.CharField(max_length=254)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Customer."""

        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        """Unicode representation of Customer."""
        return self.name

