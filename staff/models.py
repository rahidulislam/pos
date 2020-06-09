from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from branches.models import Branch
# Create your models here.

class UserManager(BaseUserManager):
    user_in_migration = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    

class Staff(AbstractUser):
    first_name = models.CharField( max_length=100, blank=False)
    last_name = models.CharField( max_length=100, blank=False)
    nid = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to="profile_photo/",blank=True, null=True)
    dob = models.DateField(default="1990-01-01", blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    employer = models.CharField(max_length=100, blank=True, null=True)
    MARTIAL_CHOICE = (
        ('single','Single'),
        ('married', 'Married'),
        ('devorce', 'Devorce'),
        ('other', 'Other'),
    )
    martial_status = models.CharField(choices=MARTIAL_CHOICE, max_length=10, default='single')
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = ("Staff")
        verbose_name_plural = ("Staffs")

    def validate_staff_email(self, email=''):
        staff = Staff.objects.get(email=email)
        if staff:
            raise ValidationError(_('%(email)s is exist'), params={'email':email})
    
    def get_short_name(self):
        return self.last_name