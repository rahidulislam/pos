from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Branch_detail", kwargs={"pk": self.pk})
