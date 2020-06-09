from django.db import models
from products.models import Products
#from 

# Create your models here.
class Sales(models.Model):
    """Model definition for Sales."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Sales."""

        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self):
        """Unicode representation of Sales."""
        pass
